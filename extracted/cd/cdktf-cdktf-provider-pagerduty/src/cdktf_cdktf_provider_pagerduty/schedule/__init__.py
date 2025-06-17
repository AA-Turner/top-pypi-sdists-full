r'''
# `pagerduty_schedule`

Refer to the Terraform Registry for docs: [`pagerduty_schedule`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule).
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


class Schedule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.schedule.Schedule",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule pagerduty_schedule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        layer: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ScheduleLayer", typing.Dict[builtins.str, typing.Any]]]],
        time_zone: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        overflow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        teams: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule pagerduty_schedule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param layer: layer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#layer Schedule#layer}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#time_zone Schedule#time_zone}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#description Schedule#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#id Schedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#name Schedule#name}.
        :param overflow: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#overflow Schedule#overflow}.
        :param teams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#teams Schedule#teams}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90d91b48269f0f51be34487a7864eaf76abb6f02df1e29e2305e645b8d6bdd2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ScheduleConfig(
            layer=layer,
            time_zone=time_zone,
            description=description,
            id=id,
            name=name,
            overflow=overflow,
            teams=teams,
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
        '''Generates CDKTF code for importing a Schedule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Schedule to import.
        :param import_from_id: The id of the existing Schedule that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Schedule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec959c583f422e2adcbe4998b38695dd918e0e873ad5cea696e63f8145f6120)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLayer")
    def put_layer(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ScheduleLayer", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de3d9c0f842433ead398684371da4807cd3422327bbdf3b262ecf17deb22bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLayer", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOverflow")
    def reset_overflow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverflow", []))

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
    @jsii.member(jsii_name="finalSchedule")
    def final_schedule(self) -> "ScheduleFinalScheduleList":
        return typing.cast("ScheduleFinalScheduleList", jsii.get(self, "finalSchedule"))

    @builtins.property
    @jsii.member(jsii_name="layer")
    def layer(self) -> "ScheduleLayerList":
        return typing.cast("ScheduleLayerList", jsii.get(self, "layer"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="layerInput")
    def layer_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ScheduleLayer"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ScheduleLayer"]]], jsii.get(self, "layerInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="overflowInput")
    def overflow_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overflowInput"))

    @builtins.property
    @jsii.member(jsii_name="teamsInput")
    def teams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "teamsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5911b8413361058c956c31332f46bb7fac5fc49e8ad942f70bbcaefba795eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9385be5d123187766b92d27a641fe1af6ea0ab39c170c781f82214a54dbc3b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0bdcf1037312be69b5ae9a2e0da195592d52cea5f3c696302b22b3a1d57e2b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overflow")
    def overflow(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overflow"))

    @overflow.setter
    def overflow(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1857fa517e626e26942ed15f789ca72bee083203fee7863612b7154ef154eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overflow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="teams")
    def teams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "teams"))

    @teams.setter
    def teams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad61cb97154cd0efe7720aed4a674f798ef35411d5fb86b089b31b9f2d256b6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb6bdbaf2b36b5814f7cec711ef172769bd0c67d1d828dd95bbf7d6ea580487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.schedule.ScheduleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "layer": "layer",
        "time_zone": "timeZone",
        "description": "description",
        "id": "id",
        "name": "name",
        "overflow": "overflow",
        "teams": "teams",
    },
)
class ScheduleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        layer: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ScheduleLayer", typing.Dict[builtins.str, typing.Any]]]],
        time_zone: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        overflow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        :param layer: layer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#layer Schedule#layer}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#time_zone Schedule#time_zone}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#description Schedule#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#id Schedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#name Schedule#name}.
        :param overflow: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#overflow Schedule#overflow}.
        :param teams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#teams Schedule#teams}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820dc386b47ca340aca6740aae2da1d409aaf27f92d82ec6500826f61521156f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument layer", value=layer, expected_type=type_hints["layer"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument overflow", value=overflow, expected_type=type_hints["overflow"])
            check_type(argname="argument teams", value=teams, expected_type=type_hints["teams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "layer": layer,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if overflow is not None:
            self._values["overflow"] = overflow
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
    def layer(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ScheduleLayer"]]:
        '''layer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#layer Schedule#layer}
        '''
        result = self._values.get("layer")
        assert result is not None, "Required property 'layer' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ScheduleLayer"]], result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#time_zone Schedule#time_zone}.'''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#description Schedule#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#id Schedule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#name Schedule#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overflow(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#overflow Schedule#overflow}.'''
        result = self._values.get("overflow")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def teams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#teams Schedule#teams}.'''
        result = self._values.get("teams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.schedule.ScheduleFinalSchedule",
    jsii_struct_bases=[],
    name_mapping={},
)
class ScheduleFinalSchedule:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleFinalSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ScheduleFinalScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.schedule.ScheduleFinalScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ddabc6d772876a915c194002f55549b5032fc5512e3e00557265de4cdc2c54f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ScheduleFinalScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e71d73a7c5e781c1a6a2db9f2439e342bb0bf28bb03a8fdbc56f572ed95d3616)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ScheduleFinalScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee8af52b7ed026a9b679dd53fb7eeb321e7ff3a650f7597bb018d61059393c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb24f6b1c6fa7eccab2bbd53d88f65bf46d0a6c7979ae704222753a046fc306f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d253c2345f95a1546822e2d03f9299a903b8ef9b40071814edc9d5efcd1b4773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ScheduleFinalScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.schedule.ScheduleFinalScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08193b561a683e18e772c57cc3303ad7cce72cf2c7940884cb75ff685c860346)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="renderedCoveragePercentage")
    def rendered_coverage_percentage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "renderedCoveragePercentage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ScheduleFinalSchedule]:
        return typing.cast(typing.Optional[ScheduleFinalSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ScheduleFinalSchedule]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95720bd6ce91195d11d2b7f73f2a61c437b19696d47a223bf9b2c491dd392ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.schedule.ScheduleLayer",
    jsii_struct_bases=[],
    name_mapping={
        "rotation_turn_length_seconds": "rotationTurnLengthSeconds",
        "rotation_virtual_start": "rotationVirtualStart",
        "start": "start",
        "users": "users",
        "end": "end",
        "name": "name",
        "restriction": "restriction",
    },
)
class ScheduleLayer:
    def __init__(
        self,
        *,
        rotation_turn_length_seconds: jsii.Number,
        rotation_virtual_start: builtins.str,
        start: builtins.str,
        users: typing.Sequence[builtins.str],
        end: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ScheduleLayerRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rotation_turn_length_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#rotation_turn_length_seconds Schedule#rotation_turn_length_seconds}.
        :param rotation_virtual_start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#rotation_virtual_start Schedule#rotation_virtual_start}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#start Schedule#start}.
        :param users: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#users Schedule#users}.
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#end Schedule#end}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#name Schedule#name}.
        :param restriction: restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#restriction Schedule#restriction}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9bf06797e1759c1c1c0f955bfd9a4ffc32703ec28b11153ddaff5ba9be323f)
            check_type(argname="argument rotation_turn_length_seconds", value=rotation_turn_length_seconds, expected_type=type_hints["rotation_turn_length_seconds"])
            check_type(argname="argument rotation_virtual_start", value=rotation_virtual_start, expected_type=type_hints["rotation_virtual_start"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument restriction", value=restriction, expected_type=type_hints["restriction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rotation_turn_length_seconds": rotation_turn_length_seconds,
            "rotation_virtual_start": rotation_virtual_start,
            "start": start,
            "users": users,
        }
        if end is not None:
            self._values["end"] = end
        if name is not None:
            self._values["name"] = name
        if restriction is not None:
            self._values["restriction"] = restriction

    @builtins.property
    def rotation_turn_length_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#rotation_turn_length_seconds Schedule#rotation_turn_length_seconds}.'''
        result = self._values.get("rotation_turn_length_seconds")
        assert result is not None, "Required property 'rotation_turn_length_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def rotation_virtual_start(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#rotation_virtual_start Schedule#rotation_virtual_start}.'''
        result = self._values.get("rotation_virtual_start")
        assert result is not None, "Required property 'rotation_virtual_start' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#start Schedule#start}.'''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def users(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#users Schedule#users}.'''
        result = self._values.get("users")
        assert result is not None, "Required property 'users' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def end(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#end Schedule#end}.'''
        result = self._values.get("end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#name Schedule#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restriction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ScheduleLayerRestriction"]]]:
        '''restriction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#restriction Schedule#restriction}
        '''
        result = self._values.get("restriction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ScheduleLayerRestriction"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleLayer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ScheduleLayerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.schedule.ScheduleLayerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3fbbe5c54c55249d628362b47be5c5455399907d09045e902a9fed62108b176)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ScheduleLayerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c863e437d6f3328e4e152a9761ae248450999598b8c77459b3916d0030d6ff7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ScheduleLayerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5fc8cfcabdefe77741b5e8ad9f2025b760693f8e27e562bce322d9975e70c42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__151d1f388a7a6e2cf42d92c03545213a3064086346a3058cbf815324d3cbd68c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__109d249fdd0e238d5f38541e5029b41da08822b6a7d8a8394d18b64924cebfeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ScheduleLayer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ScheduleLayer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ScheduleLayer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3005b0c05033eaff3c3fdc4d8be71797aedc9df0314432e0d9b1ce8bb379a4aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ScheduleLayerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.schedule.ScheduleLayerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20379d2176d159317ee744f4b5ab7fe55c6d1e7b4c95c7872e2504e46315a559)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRestriction")
    def put_restriction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ScheduleLayerRestriction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c942008173ef8b6854ed17117d50d6bcb183cc52449a001229897caf1f113fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRestriction", [value]))

    @jsii.member(jsii_name="resetEnd")
    def reset_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnd", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRestriction")
    def reset_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestriction", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="renderedCoveragePercentage")
    def rendered_coverage_percentage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "renderedCoveragePercentage"))

    @builtins.property
    @jsii.member(jsii_name="restriction")
    def restriction(self) -> "ScheduleLayerRestrictionList":
        return typing.cast("ScheduleLayerRestrictionList", jsii.get(self, "restriction"))

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictionInput")
    def restriction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ScheduleLayerRestriction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ScheduleLayerRestriction"]]], jsii.get(self, "restrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationTurnLengthSecondsInput")
    def rotation_turn_length_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rotationTurnLengthSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationVirtualStartInput")
    def rotation_virtual_start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rotationVirtualStartInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="usersInput")
    def users_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "end"))

    @end.setter
    def end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a11a4cee46b3253bace9224ba4862e5578059ba92e8a2e36b6eb63a84deaa04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c011752dd1ca069fa2b64bdfa8517db00ccb364372af9614fc4dc9804113c08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationTurnLengthSeconds")
    def rotation_turn_length_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rotationTurnLengthSeconds"))

    @rotation_turn_length_seconds.setter
    def rotation_turn_length_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37068752df0081e57931c0d67bfa2103f88fa6b77f07ad5041a6d0f37c597abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationTurnLengthSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationVirtualStart")
    def rotation_virtual_start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rotationVirtualStart"))

    @rotation_virtual_start.setter
    def rotation_virtual_start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f790b814c91419fbe02c7d464849c37633382de0c47a95108a36ba58fdf01b92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationVirtualStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "start"))

    @start.setter
    def start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e548dc31c28ed87d54de596c81a298cb4490516ea5b7e3c6b03ea68fff19341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea25f92a133319231e354d022fd279c4a43c84b71f5d75ee897c78c350afc17a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ScheduleLayer]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ScheduleLayer]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ScheduleLayer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5400b16d71f0ab537edf65526c33670644eaa3d5e039fda9b9f1432f7dd1fa60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.schedule.ScheduleLayerRestriction",
    jsii_struct_bases=[],
    name_mapping={
        "duration_seconds": "durationSeconds",
        "start_time_of_day": "startTimeOfDay",
        "type": "type",
        "start_day_of_week": "startDayOfWeek",
    },
)
class ScheduleLayerRestriction:
    def __init__(
        self,
        *,
        duration_seconds: jsii.Number,
        start_time_of_day: builtins.str,
        type: builtins.str,
        start_day_of_week: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param duration_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#duration_seconds Schedule#duration_seconds}.
        :param start_time_of_day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#start_time_of_day Schedule#start_time_of_day}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#type Schedule#type}.
        :param start_day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#start_day_of_week Schedule#start_day_of_week}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80723a079b3396e320246c86b8cd31f423d81d0eb08ef17efb52747ce5747ead)
            check_type(argname="argument duration_seconds", value=duration_seconds, expected_type=type_hints["duration_seconds"])
            check_type(argname="argument start_time_of_day", value=start_time_of_day, expected_type=type_hints["start_time_of_day"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument start_day_of_week", value=start_day_of_week, expected_type=type_hints["start_day_of_week"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "duration_seconds": duration_seconds,
            "start_time_of_day": start_time_of_day,
            "type": type,
        }
        if start_day_of_week is not None:
            self._values["start_day_of_week"] = start_day_of_week

    @builtins.property
    def duration_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#duration_seconds Schedule#duration_seconds}.'''
        result = self._values.get("duration_seconds")
        assert result is not None, "Required property 'duration_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_time_of_day(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#start_time_of_day Schedule#start_time_of_day}.'''
        result = self._values.get("start_time_of_day")
        assert result is not None, "Required property 'start_time_of_day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#type Schedule#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_day_of_week(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/schedule#start_day_of_week Schedule#start_day_of_week}.'''
        result = self._values.get("start_day_of_week")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleLayerRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ScheduleLayerRestrictionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.schedule.ScheduleLayerRestrictionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f01e34fa699e6a3676f31e33fad64fa75f21014a1eea87bd1d22ccf97a2af238)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ScheduleLayerRestrictionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc02ddcd6dfe2ffef2c3ce91caba7a1f03cf0887a03c15f2c3aa9737c3219b9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ScheduleLayerRestrictionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff29a9b802fe20f9ec04f9a9a5e1a8acaa24010fab7eda7f048e60ef56ee937)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf4d61ccb27e434470ed6167052c9e79f9cab0c3848b3c638297bfda5a0cb108)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31c54720c228caf6bb06a3a6a3ec57086c5f4ca75c0e6a91d82cfd1419706488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ScheduleLayerRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ScheduleLayerRestriction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ScheduleLayerRestriction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a8c8d553dfb7417624e58ba6441efc1e764cecda16846578c28288164b6866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ScheduleLayerRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.schedule.ScheduleLayerRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5f8446224d408ea51040e323e9066e8dc5c975350f4d2d0c3d34210ea4ca22a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetStartDayOfWeek")
    def reset_start_day_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartDayOfWeek", []))

    @builtins.property
    @jsii.member(jsii_name="durationSecondsInput")
    def duration_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="startDayOfWeekInput")
    def start_day_of_week_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startDayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeOfDayInput")
    def start_time_of_day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="durationSeconds")
    def duration_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "durationSeconds"))

    @duration_seconds.setter
    def duration_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02335a4f1d7e0bfc1ce8cb62ed324c89cbd30623800e30b874bde7bc7074ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startDayOfWeek")
    def start_day_of_week(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startDayOfWeek"))

    @start_day_of_week.setter
    def start_day_of_week(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf662fb884a01231c00aed760d45b3f31bd310ef2b6f3120b948aeac6846877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startDayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTimeOfDay")
    def start_time_of_day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTimeOfDay"))

    @start_time_of_day.setter
    def start_time_of_day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e49ffc28c6cedcd1f2c02116da756eb7a7f89e5b351fa8d17e1fc4df4a7bbca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f66b55fce108f5ea780bcbd3324143e008c6326a60e7a9a17c6ea21aa0170eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ScheduleLayerRestriction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ScheduleLayerRestriction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ScheduleLayerRestriction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc551a66e269a1890c93fe6898b15c1c7c5fde509bbdda0e331e44275f1a0d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Schedule",
    "ScheduleConfig",
    "ScheduleFinalSchedule",
    "ScheduleFinalScheduleList",
    "ScheduleFinalScheduleOutputReference",
    "ScheduleLayer",
    "ScheduleLayerList",
    "ScheduleLayerOutputReference",
    "ScheduleLayerRestriction",
    "ScheduleLayerRestrictionList",
    "ScheduleLayerRestrictionOutputReference",
]

publication.publish()

def _typecheckingstub__f90d91b48269f0f51be34487a7864eaf76abb6f02df1e29e2305e645b8d6bdd2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    layer: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ScheduleLayer, typing.Dict[builtins.str, typing.Any]]]],
    time_zone: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    overflow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__fec959c583f422e2adcbe4998b38695dd918e0e873ad5cea696e63f8145f6120(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de3d9c0f842433ead398684371da4807cd3422327bbdf3b262ecf17deb22bb5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ScheduleLayer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5911b8413361058c956c31332f46bb7fac5fc49e8ad942f70bbcaefba795eeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9385be5d123187766b92d27a641fe1af6ea0ab39c170c781f82214a54dbc3b38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bdcf1037312be69b5ae9a2e0da195592d52cea5f3c696302b22b3a1d57e2b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1857fa517e626e26942ed15f789ca72bee083203fee7863612b7154ef154eb5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad61cb97154cd0efe7720aed4a674f798ef35411d5fb86b089b31b9f2d256b6b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb6bdbaf2b36b5814f7cec711ef172769bd0c67d1d828dd95bbf7d6ea580487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820dc386b47ca340aca6740aae2da1d409aaf27f92d82ec6500826f61521156f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    layer: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ScheduleLayer, typing.Dict[builtins.str, typing.Any]]]],
    time_zone: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    overflow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    teams: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ddabc6d772876a915c194002f55549b5032fc5512e3e00557265de4cdc2c54f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71d73a7c5e781c1a6a2db9f2439e342bb0bf28bb03a8fdbc56f572ed95d3616(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee8af52b7ed026a9b679dd53fb7eeb321e7ff3a650f7597bb018d61059393c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb24f6b1c6fa7eccab2bbd53d88f65bf46d0a6c7979ae704222753a046fc306f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d253c2345f95a1546822e2d03f9299a903b8ef9b40071814edc9d5efcd1b4773(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08193b561a683e18e772c57cc3303ad7cce72cf2c7940884cb75ff685c860346(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95720bd6ce91195d11d2b7f73f2a61c437b19696d47a223bf9b2c491dd392ff(
    value: typing.Optional[ScheduleFinalSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9bf06797e1759c1c1c0f955bfd9a4ffc32703ec28b11153ddaff5ba9be323f(
    *,
    rotation_turn_length_seconds: jsii.Number,
    rotation_virtual_start: builtins.str,
    start: builtins.str,
    users: typing.Sequence[builtins.str],
    end: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ScheduleLayerRestriction, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fbbe5c54c55249d628362b47be5c5455399907d09045e902a9fed62108b176(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c863e437d6f3328e4e152a9761ae248450999598b8c77459b3916d0030d6ff7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5fc8cfcabdefe77741b5e8ad9f2025b760693f8e27e562bce322d9975e70c42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151d1f388a7a6e2cf42d92c03545213a3064086346a3058cbf815324d3cbd68c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109d249fdd0e238d5f38541e5029b41da08822b6a7d8a8394d18b64924cebfeb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3005b0c05033eaff3c3fdc4d8be71797aedc9df0314432e0d9b1ce8bb379a4aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ScheduleLayer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20379d2176d159317ee744f4b5ab7fe55c6d1e7b4c95c7872e2504e46315a559(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c942008173ef8b6854ed17117d50d6bcb183cc52449a001229897caf1f113fa2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ScheduleLayerRestriction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a11a4cee46b3253bace9224ba4862e5578059ba92e8a2e36b6eb63a84deaa04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c011752dd1ca069fa2b64bdfa8517db00ccb364372af9614fc4dc9804113c08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37068752df0081e57931c0d67bfa2103f88fa6b77f07ad5041a6d0f37c597abb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f790b814c91419fbe02c7d464849c37633382de0c47a95108a36ba58fdf01b92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e548dc31c28ed87d54de596c81a298cb4490516ea5b7e3c6b03ea68fff19341(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea25f92a133319231e354d022fd279c4a43c84b71f5d75ee897c78c350afc17a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5400b16d71f0ab537edf65526c33670644eaa3d5e039fda9b9f1432f7dd1fa60(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ScheduleLayer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80723a079b3396e320246c86b8cd31f423d81d0eb08ef17efb52747ce5747ead(
    *,
    duration_seconds: jsii.Number,
    start_time_of_day: builtins.str,
    type: builtins.str,
    start_day_of_week: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01e34fa699e6a3676f31e33fad64fa75f21014a1eea87bd1d22ccf97a2af238(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc02ddcd6dfe2ffef2c3ce91caba7a1f03cf0887a03c15f2c3aa9737c3219b9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff29a9b802fe20f9ec04f9a9a5e1a8acaa24010fab7eda7f048e60ef56ee937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4d61ccb27e434470ed6167052c9e79f9cab0c3848b3c638297bfda5a0cb108(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c54720c228caf6bb06a3a6a3ec57086c5f4ca75c0e6a91d82cfd1419706488(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a8c8d553dfb7417624e58ba6441efc1e764cecda16846578c28288164b6866(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ScheduleLayerRestriction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f8446224d408ea51040e323e9066e8dc5c975350f4d2d0c3d34210ea4ca22a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02335a4f1d7e0bfc1ce8cb62ed324c89cbd30623800e30b874bde7bc7074ae2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf662fb884a01231c00aed760d45b3f31bd310ef2b6f3120b948aeac6846877(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e49ffc28c6cedcd1f2c02116da756eb7a7f89e5b351fa8d17e1fc4df4a7bbca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66b55fce108f5ea780bcbd3324143e008c6326a60e7a9a17c6ea21aa0170eb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc551a66e269a1890c93fe6898b15c1c7c5fde509bbdda0e331e44275f1a0d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ScheduleLayerRestriction]],
) -> None:
    """Type checking stubs"""
    pass
