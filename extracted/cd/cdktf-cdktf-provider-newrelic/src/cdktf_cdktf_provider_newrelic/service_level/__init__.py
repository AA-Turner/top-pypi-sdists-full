r'''
# `newrelic_service_level`

Refer to the Terraform Registry for docs: [`newrelic_service_level`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level).
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


class ServiceLevel(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevel",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level newrelic_service_level}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        events: typing.Union["ServiceLevelEvents", typing.Dict[builtins.str, typing.Any]],
        guid: builtins.str,
        name: builtins.str,
        objective: typing.Union["ServiceLevelObjective", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level newrelic_service_level} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param events: events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#events ServiceLevel#events}
        :param guid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#guid ServiceLevel#guid}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#name ServiceLevel#name}.
        :param objective: objective block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#objective ServiceLevel#objective}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#description ServiceLevel#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#id ServiceLevel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63476dcca6c12f410fba2b0b58d3d61fe6cbc24e408f95e1b9dde2ddd7e67c67)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceLevelConfig(
            events=events,
            guid=guid,
            name=name,
            objective=objective,
            description=description,
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
        '''Generates CDKTF code for importing a ServiceLevel resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ServiceLevel to import.
        :param import_from_id: The id of the existing ServiceLevel that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ServiceLevel to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7de8ade568706777fbebda389d8fe73913d16787c3f3bdfb0575edd968f82b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEvents")
    def put_events(
        self,
        *,
        account_id: jsii.Number,
        valid_events: typing.Union["ServiceLevelEventsValidEvents", typing.Dict[builtins.str, typing.Any]],
        bad_events: typing.Optional[typing.Union["ServiceLevelEventsBadEvents", typing.Dict[builtins.str, typing.Any]]] = None,
        good_events: typing.Optional[typing.Union["ServiceLevelEventsGoodEvents", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#account_id ServiceLevel#account_id}.
        :param valid_events: valid_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#valid_events ServiceLevel#valid_events}
        :param bad_events: bad_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#bad_events ServiceLevel#bad_events}
        :param good_events: good_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#good_events ServiceLevel#good_events}
        '''
        value = ServiceLevelEvents(
            account_id=account_id,
            valid_events=valid_events,
            bad_events=bad_events,
            good_events=good_events,
        )

        return typing.cast(None, jsii.invoke(self, "putEvents", [value]))

    @jsii.member(jsii_name="putObjective")
    def put_objective(
        self,
        *,
        target: jsii.Number,
        time_window: typing.Union["ServiceLevelObjectiveTimeWindow", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#target ServiceLevel#target}.
        :param time_window: time_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#time_window ServiceLevel#time_window}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#description ServiceLevel#description}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#name ServiceLevel#name}.
        '''
        value = ServiceLevelObjective(
            target=target, time_window=time_window, description=description, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putObjective", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

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
    @jsii.member(jsii_name="events")
    def events(self) -> "ServiceLevelEventsOutputReference":
        return typing.cast("ServiceLevelEventsOutputReference", jsii.get(self, "events"))

    @builtins.property
    @jsii.member(jsii_name="objective")
    def objective(self) -> "ServiceLevelObjectiveOutputReference":
        return typing.cast("ServiceLevelObjectiveOutputReference", jsii.get(self, "objective"))

    @builtins.property
    @jsii.member(jsii_name="sliGuid")
    def sli_guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sliGuid"))

    @builtins.property
    @jsii.member(jsii_name="sliId")
    def sli_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sliId"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventsInput")
    def events_input(self) -> typing.Optional["ServiceLevelEvents"]:
        return typing.cast(typing.Optional["ServiceLevelEvents"], jsii.get(self, "eventsInput"))

    @builtins.property
    @jsii.member(jsii_name="guidInput")
    def guid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "guidInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectiveInput")
    def objective_input(self) -> typing.Optional["ServiceLevelObjective"]:
        return typing.cast(typing.Optional["ServiceLevelObjective"], jsii.get(self, "objectiveInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac466664e39127beccf9d6af6a4cc30f505a249c590e63ca7f96d34ee1c0718c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guid")
    def guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guid"))

    @guid.setter
    def guid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c40f4e4220646a5b5fef08ab8f99c77697b5087dbf384126dc53ff6445bd7fc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2429fe236c8a7c4ff13391b9f8d7bea17dd67c7553bb35b0d0e8b51afc9e0203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a7d682edabbb1c0ac985154cad8e50335063f7f82d487714c6bc6a05b8b81d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "events": "events",
        "guid": "guid",
        "name": "name",
        "objective": "objective",
        "description": "description",
        "id": "id",
    },
)
class ServiceLevelConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        events: typing.Union["ServiceLevelEvents", typing.Dict[builtins.str, typing.Any]],
        guid: builtins.str,
        name: builtins.str,
        objective: typing.Union["ServiceLevelObjective", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
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
        :param events: events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#events ServiceLevel#events}
        :param guid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#guid ServiceLevel#guid}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#name ServiceLevel#name}.
        :param objective: objective block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#objective ServiceLevel#objective}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#description ServiceLevel#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#id ServiceLevel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(events, dict):
            events = ServiceLevelEvents(**events)
        if isinstance(objective, dict):
            objective = ServiceLevelObjective(**objective)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed11a849c998def40d353dbdc59c1ee4ba95fde523da099f71fee6082e487e81)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument guid", value=guid, expected_type=type_hints["guid"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument objective", value=objective, expected_type=type_hints["objective"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "events": events,
            "guid": guid,
            "name": name,
            "objective": objective,
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
    def events(self) -> "ServiceLevelEvents":
        '''events block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#events ServiceLevel#events}
        '''
        result = self._values.get("events")
        assert result is not None, "Required property 'events' is missing"
        return typing.cast("ServiceLevelEvents", result)

    @builtins.property
    def guid(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#guid ServiceLevel#guid}.'''
        result = self._values.get("guid")
        assert result is not None, "Required property 'guid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#name ServiceLevel#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def objective(self) -> "ServiceLevelObjective":
        '''objective block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#objective ServiceLevel#objective}
        '''
        result = self._values.get("objective")
        assert result is not None, "Required property 'objective' is missing"
        return typing.cast("ServiceLevelObjective", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#description ServiceLevel#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#id ServiceLevel#id}.

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
        return "ServiceLevelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEvents",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "valid_events": "validEvents",
        "bad_events": "badEvents",
        "good_events": "goodEvents",
    },
)
class ServiceLevelEvents:
    def __init__(
        self,
        *,
        account_id: jsii.Number,
        valid_events: typing.Union["ServiceLevelEventsValidEvents", typing.Dict[builtins.str, typing.Any]],
        bad_events: typing.Optional[typing.Union["ServiceLevelEventsBadEvents", typing.Dict[builtins.str, typing.Any]]] = None,
        good_events: typing.Optional[typing.Union["ServiceLevelEventsGoodEvents", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#account_id ServiceLevel#account_id}.
        :param valid_events: valid_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#valid_events ServiceLevel#valid_events}
        :param bad_events: bad_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#bad_events ServiceLevel#bad_events}
        :param good_events: good_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#good_events ServiceLevel#good_events}
        '''
        if isinstance(valid_events, dict):
            valid_events = ServiceLevelEventsValidEvents(**valid_events)
        if isinstance(bad_events, dict):
            bad_events = ServiceLevelEventsBadEvents(**bad_events)
        if isinstance(good_events, dict):
            good_events = ServiceLevelEventsGoodEvents(**good_events)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16fed349c47b4dc9012248f526f151b88047a6790b6ac488a42c7c4f94ba7745)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument valid_events", value=valid_events, expected_type=type_hints["valid_events"])
            check_type(argname="argument bad_events", value=bad_events, expected_type=type_hints["bad_events"])
            check_type(argname="argument good_events", value=good_events, expected_type=type_hints["good_events"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "valid_events": valid_events,
        }
        if bad_events is not None:
            self._values["bad_events"] = bad_events
        if good_events is not None:
            self._values["good_events"] = good_events

    @builtins.property
    def account_id(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#account_id ServiceLevel#account_id}.'''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def valid_events(self) -> "ServiceLevelEventsValidEvents":
        '''valid_events block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#valid_events ServiceLevel#valid_events}
        '''
        result = self._values.get("valid_events")
        assert result is not None, "Required property 'valid_events' is missing"
        return typing.cast("ServiceLevelEventsValidEvents", result)

    @builtins.property
    def bad_events(self) -> typing.Optional["ServiceLevelEventsBadEvents"]:
        '''bad_events block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#bad_events ServiceLevel#bad_events}
        '''
        result = self._values.get("bad_events")
        return typing.cast(typing.Optional["ServiceLevelEventsBadEvents"], result)

    @builtins.property
    def good_events(self) -> typing.Optional["ServiceLevelEventsGoodEvents"]:
        '''good_events block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#good_events ServiceLevel#good_events}
        '''
        result = self._values.get("good_events")
        return typing.cast(typing.Optional["ServiceLevelEventsGoodEvents"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelEvents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEventsBadEvents",
    jsii_struct_bases=[],
    name_mapping={"from_": "from", "select": "select", "where": "where"},
)
class ServiceLevelEventsBadEvents:
    def __init__(
        self,
        *,
        from_: builtins.str,
        select: typing.Optional[typing.Union["ServiceLevelEventsBadEventsSelect", typing.Dict[builtins.str, typing.Any]]] = None,
        where: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#from ServiceLevel#from}.
        :param select: select block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#select ServiceLevel#select}
        :param where: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#where ServiceLevel#where}.
        '''
        if isinstance(select, dict):
            select = ServiceLevelEventsBadEventsSelect(**select)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f226aa354f3da3854346667fa02ef1c67a79d11e900658730768f01ad263d21c)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument select", value=select, expected_type=type_hints["select"])
            check_type(argname="argument where", value=where, expected_type=type_hints["where"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "from_": from_,
        }
        if select is not None:
            self._values["select"] = select
        if where is not None:
            self._values["where"] = where

    @builtins.property
    def from_(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#from ServiceLevel#from}.'''
        result = self._values.get("from_")
        assert result is not None, "Required property 'from_' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def select(self) -> typing.Optional["ServiceLevelEventsBadEventsSelect"]:
        '''select block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#select ServiceLevel#select}
        '''
        result = self._values.get("select")
        return typing.cast(typing.Optional["ServiceLevelEventsBadEventsSelect"], result)

    @builtins.property
    def where(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#where ServiceLevel#where}.'''
        result = self._values.get("where")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelEventsBadEvents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelEventsBadEventsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEventsBadEventsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12e2e63bd7d50f86c87d54beb25cc6183ea39af4dd4ee0cb2a291206dd46cc35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelect")
    def put_select(
        self,
        *,
        function: builtins.str,
        attribute: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#function ServiceLevel#function}.
        :param attribute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#attribute ServiceLevel#attribute}.
        :param threshold: The event threshold to use in the SELECT clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#threshold ServiceLevel#threshold}
        '''
        value = ServiceLevelEventsBadEventsSelect(
            function=function, attribute=attribute, threshold=threshold
        )

        return typing.cast(None, jsii.invoke(self, "putSelect", [value]))

    @jsii.member(jsii_name="resetSelect")
    def reset_select(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelect", []))

    @jsii.member(jsii_name="resetWhere")
    def reset_where(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhere", []))

    @builtins.property
    @jsii.member(jsii_name="select")
    def select(self) -> "ServiceLevelEventsBadEventsSelectOutputReference":
        return typing.cast("ServiceLevelEventsBadEventsSelectOutputReference", jsii.get(self, "select"))

    @builtins.property
    @jsii.member(jsii_name="fromInput")
    def from_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromInput"))

    @builtins.property
    @jsii.member(jsii_name="selectInput")
    def select_input(self) -> typing.Optional["ServiceLevelEventsBadEventsSelect"]:
        return typing.cast(typing.Optional["ServiceLevelEventsBadEventsSelect"], jsii.get(self, "selectInput"))

    @builtins.property
    @jsii.member(jsii_name="whereInput")
    def where_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "whereInput"))

    @builtins.property
    @jsii.member(jsii_name="from")
    def from_(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "from"))

    @from_.setter
    def from_(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb0a6f6ac73e8d0b838cb95b68849bcb097c5eabc1d9af015c4fca6e790037d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "from", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="where")
    def where(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "where"))

    @where.setter
    def where(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d51f376d840e0627e6e8dd4b0328da059b3eaa0bcdef57d8a0ccf72e823fef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "where", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceLevelEventsBadEvents]:
        return typing.cast(typing.Optional[ServiceLevelEventsBadEvents], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelEventsBadEvents],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec85e29b5404c0795d92547d079dc047365547290c074a9005dffc6a3f306459)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEventsBadEventsSelect",
    jsii_struct_bases=[],
    name_mapping={
        "function": "function",
        "attribute": "attribute",
        "threshold": "threshold",
    },
)
class ServiceLevelEventsBadEventsSelect:
    def __init__(
        self,
        *,
        function: builtins.str,
        attribute: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#function ServiceLevel#function}.
        :param attribute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#attribute ServiceLevel#attribute}.
        :param threshold: The event threshold to use in the SELECT clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#threshold ServiceLevel#threshold}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3e010a766d974590ea8e3dacb90a49454df4697492aef625be94a9aee8480b)
            check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function": function,
        }
        if attribute is not None:
            self._values["attribute"] = attribute
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def function(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#function ServiceLevel#function}.'''
        result = self._values.get("function")
        assert result is not None, "Required property 'function' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#attribute ServiceLevel#attribute}.'''
        result = self._values.get("attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The event threshold to use in the SELECT clause.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#threshold ServiceLevel#threshold}
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelEventsBadEventsSelect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelEventsBadEventsSelectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEventsBadEventsSelectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6beb9977fb9622f65253797306f9ed0e3cd81473577c4d8f2f54f2f85e284988)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAttribute")
    def reset_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttribute", []))

    @jsii.member(jsii_name="resetThreshold")
    def reset_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreshold", []))

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="functionInput")
    def function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0465fc92ef0f69f84ae296bb94516b73aa2b59690507103f09d332c7a63375d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "function"))

    @function.setter
    def function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4b39553c930810137eb3b3a8300272fca4890880c2f11f908cf9bdcd71fa9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "function", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__756ac5be4115d542855924f63b231e3e52bfe71910f192345e26a8355fcc74a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceLevelEventsBadEventsSelect]:
        return typing.cast(typing.Optional[ServiceLevelEventsBadEventsSelect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelEventsBadEventsSelect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246b07d89b1820dda9947a0fbe6e9c8d3f365a21f8c2840855ae41cd6c6f4856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEventsGoodEvents",
    jsii_struct_bases=[],
    name_mapping={"from_": "from", "select": "select", "where": "where"},
)
class ServiceLevelEventsGoodEvents:
    def __init__(
        self,
        *,
        from_: builtins.str,
        select: typing.Optional[typing.Union["ServiceLevelEventsGoodEventsSelect", typing.Dict[builtins.str, typing.Any]]] = None,
        where: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#from ServiceLevel#from}.
        :param select: select block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#select ServiceLevel#select}
        :param where: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#where ServiceLevel#where}.
        '''
        if isinstance(select, dict):
            select = ServiceLevelEventsGoodEventsSelect(**select)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8edabd1d65671aa6bc294c76b7daf127f10140766bdc36cbe19ed65086200db)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument select", value=select, expected_type=type_hints["select"])
            check_type(argname="argument where", value=where, expected_type=type_hints["where"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "from_": from_,
        }
        if select is not None:
            self._values["select"] = select
        if where is not None:
            self._values["where"] = where

    @builtins.property
    def from_(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#from ServiceLevel#from}.'''
        result = self._values.get("from_")
        assert result is not None, "Required property 'from_' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def select(self) -> typing.Optional["ServiceLevelEventsGoodEventsSelect"]:
        '''select block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#select ServiceLevel#select}
        '''
        result = self._values.get("select")
        return typing.cast(typing.Optional["ServiceLevelEventsGoodEventsSelect"], result)

    @builtins.property
    def where(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#where ServiceLevel#where}.'''
        result = self._values.get("where")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelEventsGoodEvents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelEventsGoodEventsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEventsGoodEventsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e9c796b90359b55f12bf99e014b8b5a228572551e2890f6cb5b32153863c28f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelect")
    def put_select(
        self,
        *,
        function: builtins.str,
        attribute: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#function ServiceLevel#function}.
        :param attribute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#attribute ServiceLevel#attribute}.
        :param threshold: The event threshold to use in the SELECT clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#threshold ServiceLevel#threshold}
        '''
        value = ServiceLevelEventsGoodEventsSelect(
            function=function, attribute=attribute, threshold=threshold
        )

        return typing.cast(None, jsii.invoke(self, "putSelect", [value]))

    @jsii.member(jsii_name="resetSelect")
    def reset_select(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelect", []))

    @jsii.member(jsii_name="resetWhere")
    def reset_where(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhere", []))

    @builtins.property
    @jsii.member(jsii_name="select")
    def select(self) -> "ServiceLevelEventsGoodEventsSelectOutputReference":
        return typing.cast("ServiceLevelEventsGoodEventsSelectOutputReference", jsii.get(self, "select"))

    @builtins.property
    @jsii.member(jsii_name="fromInput")
    def from_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromInput"))

    @builtins.property
    @jsii.member(jsii_name="selectInput")
    def select_input(self) -> typing.Optional["ServiceLevelEventsGoodEventsSelect"]:
        return typing.cast(typing.Optional["ServiceLevelEventsGoodEventsSelect"], jsii.get(self, "selectInput"))

    @builtins.property
    @jsii.member(jsii_name="whereInput")
    def where_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "whereInput"))

    @builtins.property
    @jsii.member(jsii_name="from")
    def from_(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "from"))

    @from_.setter
    def from_(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a354f46ff97d5bf4afad9e63c8dae936e22d172b5405d7571364910bda3c4764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "from", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="where")
    def where(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "where"))

    @where.setter
    def where(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2b8254a60421e9bcd0c4fef98c003953ec81d7d64ea157592d72af91839f34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "where", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceLevelEventsGoodEvents]:
        return typing.cast(typing.Optional[ServiceLevelEventsGoodEvents], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelEventsGoodEvents],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20dbf8dc10e5608af9100bdb782df97647afbf7cbc1124f413d53a0b62383bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEventsGoodEventsSelect",
    jsii_struct_bases=[],
    name_mapping={
        "function": "function",
        "attribute": "attribute",
        "threshold": "threshold",
    },
)
class ServiceLevelEventsGoodEventsSelect:
    def __init__(
        self,
        *,
        function: builtins.str,
        attribute: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#function ServiceLevel#function}.
        :param attribute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#attribute ServiceLevel#attribute}.
        :param threshold: The event threshold to use in the SELECT clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#threshold ServiceLevel#threshold}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff02bfd1a99e9d43dcfbf7e9d76999cde19b73b2db1c9cb6ef70c0e369bbf8e)
            check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function": function,
        }
        if attribute is not None:
            self._values["attribute"] = attribute
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def function(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#function ServiceLevel#function}.'''
        result = self._values.get("function")
        assert result is not None, "Required property 'function' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#attribute ServiceLevel#attribute}.'''
        result = self._values.get("attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The event threshold to use in the SELECT clause.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#threshold ServiceLevel#threshold}
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelEventsGoodEventsSelect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelEventsGoodEventsSelectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEventsGoodEventsSelectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6f65a7a475cfd972e95d57c0f06a465a45bdb957446e2dd3f1510773ab7dc3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAttribute")
    def reset_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttribute", []))

    @jsii.member(jsii_name="resetThreshold")
    def reset_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreshold", []))

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="functionInput")
    def function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__219d9d577de36c6f38f06f665d5b4488c1203ae62385c403b020b33fe5f47a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "function"))

    @function.setter
    def function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b755953a95d0a397515b959b74b0486396fbadaafada28ee90bd325a7df69cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "function", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc1e82e6bb33542cdb189499bad935419dda5aa6ca5011315ebc97eca2472c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceLevelEventsGoodEventsSelect]:
        return typing.cast(typing.Optional[ServiceLevelEventsGoodEventsSelect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelEventsGoodEventsSelect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721b1f4b1ff43b5d56894e35e6f4539ef47633248bcbb711003adbb80e6bef48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceLevelEventsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEventsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46355e76deb8bf790af2ecf7ac778e19cf9cee75bb5a37c18bb80cbe2d5d1fde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBadEvents")
    def put_bad_events(
        self,
        *,
        from_: builtins.str,
        select: typing.Optional[typing.Union[ServiceLevelEventsBadEventsSelect, typing.Dict[builtins.str, typing.Any]]] = None,
        where: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#from ServiceLevel#from}.
        :param select: select block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#select ServiceLevel#select}
        :param where: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#where ServiceLevel#where}.
        '''
        value = ServiceLevelEventsBadEvents(from_=from_, select=select, where=where)

        return typing.cast(None, jsii.invoke(self, "putBadEvents", [value]))

    @jsii.member(jsii_name="putGoodEvents")
    def put_good_events(
        self,
        *,
        from_: builtins.str,
        select: typing.Optional[typing.Union[ServiceLevelEventsGoodEventsSelect, typing.Dict[builtins.str, typing.Any]]] = None,
        where: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#from ServiceLevel#from}.
        :param select: select block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#select ServiceLevel#select}
        :param where: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#where ServiceLevel#where}.
        '''
        value = ServiceLevelEventsGoodEvents(from_=from_, select=select, where=where)

        return typing.cast(None, jsii.invoke(self, "putGoodEvents", [value]))

    @jsii.member(jsii_name="putValidEvents")
    def put_valid_events(
        self,
        *,
        from_: builtins.str,
        select: typing.Optional[typing.Union["ServiceLevelEventsValidEventsSelect", typing.Dict[builtins.str, typing.Any]]] = None,
        where: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#from ServiceLevel#from}.
        :param select: select block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#select ServiceLevel#select}
        :param where: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#where ServiceLevel#where}.
        '''
        value = ServiceLevelEventsValidEvents(from_=from_, select=select, where=where)

        return typing.cast(None, jsii.invoke(self, "putValidEvents", [value]))

    @jsii.member(jsii_name="resetBadEvents")
    def reset_bad_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBadEvents", []))

    @jsii.member(jsii_name="resetGoodEvents")
    def reset_good_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoodEvents", []))

    @builtins.property
    @jsii.member(jsii_name="badEvents")
    def bad_events(self) -> ServiceLevelEventsBadEventsOutputReference:
        return typing.cast(ServiceLevelEventsBadEventsOutputReference, jsii.get(self, "badEvents"))

    @builtins.property
    @jsii.member(jsii_name="goodEvents")
    def good_events(self) -> ServiceLevelEventsGoodEventsOutputReference:
        return typing.cast(ServiceLevelEventsGoodEventsOutputReference, jsii.get(self, "goodEvents"))

    @builtins.property
    @jsii.member(jsii_name="validEvents")
    def valid_events(self) -> "ServiceLevelEventsValidEventsOutputReference":
        return typing.cast("ServiceLevelEventsValidEventsOutputReference", jsii.get(self, "validEvents"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="badEventsInput")
    def bad_events_input(self) -> typing.Optional[ServiceLevelEventsBadEvents]:
        return typing.cast(typing.Optional[ServiceLevelEventsBadEvents], jsii.get(self, "badEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="goodEventsInput")
    def good_events_input(self) -> typing.Optional[ServiceLevelEventsGoodEvents]:
        return typing.cast(typing.Optional[ServiceLevelEventsGoodEvents], jsii.get(self, "goodEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="validEventsInput")
    def valid_events_input(self) -> typing.Optional["ServiceLevelEventsValidEvents"]:
        return typing.cast(typing.Optional["ServiceLevelEventsValidEvents"], jsii.get(self, "validEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d1e064b91227f92ac1b485c1fa277541096bf53b2ff2e49ea558f2d0859d3b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceLevelEvents]:
        return typing.cast(typing.Optional[ServiceLevelEvents], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceLevelEvents]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a847dbaba7e277a0fb6e2309bffe18fcc937a86eabce205ac72407ff78de5086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEventsValidEvents",
    jsii_struct_bases=[],
    name_mapping={"from_": "from", "select": "select", "where": "where"},
)
class ServiceLevelEventsValidEvents:
    def __init__(
        self,
        *,
        from_: builtins.str,
        select: typing.Optional[typing.Union["ServiceLevelEventsValidEventsSelect", typing.Dict[builtins.str, typing.Any]]] = None,
        where: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#from ServiceLevel#from}.
        :param select: select block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#select ServiceLevel#select}
        :param where: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#where ServiceLevel#where}.
        '''
        if isinstance(select, dict):
            select = ServiceLevelEventsValidEventsSelect(**select)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90407512972bcdfbae50767b5387f1ed11aaa209e379e9481f2347b7417deca)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument select", value=select, expected_type=type_hints["select"])
            check_type(argname="argument where", value=where, expected_type=type_hints["where"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "from_": from_,
        }
        if select is not None:
            self._values["select"] = select
        if where is not None:
            self._values["where"] = where

    @builtins.property
    def from_(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#from ServiceLevel#from}.'''
        result = self._values.get("from_")
        assert result is not None, "Required property 'from_' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def select(self) -> typing.Optional["ServiceLevelEventsValidEventsSelect"]:
        '''select block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#select ServiceLevel#select}
        '''
        result = self._values.get("select")
        return typing.cast(typing.Optional["ServiceLevelEventsValidEventsSelect"], result)

    @builtins.property
    def where(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#where ServiceLevel#where}.'''
        result = self._values.get("where")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelEventsValidEvents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelEventsValidEventsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEventsValidEventsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ea711e534ff2dcae7d7dbd0bbcd5e501fe3c0e1b6b703891b18004858b04c90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelect")
    def put_select(
        self,
        *,
        function: builtins.str,
        attribute: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#function ServiceLevel#function}.
        :param attribute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#attribute ServiceLevel#attribute}.
        :param threshold: The event threshold to use in the SELECT clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#threshold ServiceLevel#threshold}
        '''
        value = ServiceLevelEventsValidEventsSelect(
            function=function, attribute=attribute, threshold=threshold
        )

        return typing.cast(None, jsii.invoke(self, "putSelect", [value]))

    @jsii.member(jsii_name="resetSelect")
    def reset_select(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelect", []))

    @jsii.member(jsii_name="resetWhere")
    def reset_where(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhere", []))

    @builtins.property
    @jsii.member(jsii_name="select")
    def select(self) -> "ServiceLevelEventsValidEventsSelectOutputReference":
        return typing.cast("ServiceLevelEventsValidEventsSelectOutputReference", jsii.get(self, "select"))

    @builtins.property
    @jsii.member(jsii_name="fromInput")
    def from_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromInput"))

    @builtins.property
    @jsii.member(jsii_name="selectInput")
    def select_input(self) -> typing.Optional["ServiceLevelEventsValidEventsSelect"]:
        return typing.cast(typing.Optional["ServiceLevelEventsValidEventsSelect"], jsii.get(self, "selectInput"))

    @builtins.property
    @jsii.member(jsii_name="whereInput")
    def where_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "whereInput"))

    @builtins.property
    @jsii.member(jsii_name="from")
    def from_(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "from"))

    @from_.setter
    def from_(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025ea098b1da9ea8ce7d80550aa388f4bf397de373a318ab4d0c8d52914f4cc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "from", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="where")
    def where(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "where"))

    @where.setter
    def where(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ba5a112db8ced0bd89c7418c1872c4d42c486847558ee7de4c43e27c742e7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "where", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceLevelEventsValidEvents]:
        return typing.cast(typing.Optional[ServiceLevelEventsValidEvents], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelEventsValidEvents],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa67762b0cb32a0ee67195fc595ae7891bc29ca23b8213a7f628b5dd95a38683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEventsValidEventsSelect",
    jsii_struct_bases=[],
    name_mapping={
        "function": "function",
        "attribute": "attribute",
        "threshold": "threshold",
    },
)
class ServiceLevelEventsValidEventsSelect:
    def __init__(
        self,
        *,
        function: builtins.str,
        attribute: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#function ServiceLevel#function}.
        :param attribute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#attribute ServiceLevel#attribute}.
        :param threshold: The event threshold to use in the SELECT clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#threshold ServiceLevel#threshold}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31ae9ce08b6b6caf50215fa131116d277a209612270b24dbceb23651d8e2516)
            check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function": function,
        }
        if attribute is not None:
            self._values["attribute"] = attribute
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def function(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#function ServiceLevel#function}.'''
        result = self._values.get("function")
        assert result is not None, "Required property 'function' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#attribute ServiceLevel#attribute}.'''
        result = self._values.get("attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The event threshold to use in the SELECT clause.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#threshold ServiceLevel#threshold}
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelEventsValidEventsSelect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelEventsValidEventsSelectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelEventsValidEventsSelectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a51bbe89d925c41a9b1e7dd0a29651f62ce4b70e1f554e45585857bc205f7317)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAttribute")
    def reset_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttribute", []))

    @jsii.member(jsii_name="resetThreshold")
    def reset_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreshold", []))

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="functionInput")
    def function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f84f6d66d78947c88e9de4553108c51dff4a7d83d5730fb77b38748e953bbfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "function"))

    @function.setter
    def function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa354278f58cb1bc2a4949aedc55c12a835298364c7c8f283b8a89154342160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "function", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df0a8af3dee4ba5ba2373b94fca9ee488848eacdd55f381370749dc5ae9f013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceLevelEventsValidEventsSelect]:
        return typing.cast(typing.Optional[ServiceLevelEventsValidEventsSelect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelEventsValidEventsSelect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfcab24df28d6ae5a0aeaec4d785387063a8690de64a0db80646dabe58313e43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelObjective",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "time_window": "timeWindow",
        "description": "description",
        "name": "name",
    },
)
class ServiceLevelObjective:
    def __init__(
        self,
        *,
        target: jsii.Number,
        time_window: typing.Union["ServiceLevelObjectiveTimeWindow", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#target ServiceLevel#target}.
        :param time_window: time_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#time_window ServiceLevel#time_window}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#description ServiceLevel#description}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#name ServiceLevel#name}.
        '''
        if isinstance(time_window, dict):
            time_window = ServiceLevelObjectiveTimeWindow(**time_window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2129b23dca73e5824bc883ec99252463b54fa6b8812b670f9cd30124eb3e6504)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument time_window", value=time_window, expected_type=type_hints["time_window"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
            "time_window": time_window,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def target(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#target ServiceLevel#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def time_window(self) -> "ServiceLevelObjectiveTimeWindow":
        '''time_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#time_window ServiceLevel#time_window}
        '''
        result = self._values.get("time_window")
        assert result is not None, "Required property 'time_window' is missing"
        return typing.cast("ServiceLevelObjectiveTimeWindow", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#description ServiceLevel#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#name ServiceLevel#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjective(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelObjectiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelObjectiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0565ff2ab7edcc1ee366052c48b4a207a3fb50bd4ba2aa90f28e99f271cab8cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTimeWindow")
    def put_time_window(
        self,
        *,
        rolling: typing.Union["ServiceLevelObjectiveTimeWindowRolling", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param rolling: rolling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#rolling ServiceLevel#rolling}
        '''
        value = ServiceLevelObjectiveTimeWindow(rolling=rolling)

        return typing.cast(None, jsii.invoke(self, "putTimeWindow", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="timeWindow")
    def time_window(self) -> "ServiceLevelObjectiveTimeWindowOutputReference":
        return typing.cast("ServiceLevelObjectiveTimeWindowOutputReference", jsii.get(self, "timeWindow"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeWindowInput")
    def time_window_input(self) -> typing.Optional["ServiceLevelObjectiveTimeWindow"]:
        return typing.cast(typing.Optional["ServiceLevelObjectiveTimeWindow"], jsii.get(self, "timeWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94f4592414356bf5e2f2a0fea8b85441d7f481db57718b7c9ec15334071c0048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4abba432439a67e09a322260e848c83deea2b1f44d45900d2558953a5162c182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96e756a503d032985a4a344e4d9dc174bed038b04403bf612f2248cee114aaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceLevelObjective]:
        return typing.cast(typing.Optional[ServiceLevelObjective], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceLevelObjective]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7243cb0c0f84b95ebbcc3e72e4ec5addbfdddd6bfd2709f303f737a9ef036e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelObjectiveTimeWindow",
    jsii_struct_bases=[],
    name_mapping={"rolling": "rolling"},
)
class ServiceLevelObjectiveTimeWindow:
    def __init__(
        self,
        *,
        rolling: typing.Union["ServiceLevelObjectiveTimeWindowRolling", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param rolling: rolling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#rolling ServiceLevel#rolling}
        '''
        if isinstance(rolling, dict):
            rolling = ServiceLevelObjectiveTimeWindowRolling(**rolling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034692e62689dd89d0d545f4a280fe4bc97241633123180463f446ab69c660d6)
            check_type(argname="argument rolling", value=rolling, expected_type=type_hints["rolling"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rolling": rolling,
        }

    @builtins.property
    def rolling(self) -> "ServiceLevelObjectiveTimeWindowRolling":
        '''rolling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#rolling ServiceLevel#rolling}
        '''
        result = self._values.get("rolling")
        assert result is not None, "Required property 'rolling' is missing"
        return typing.cast("ServiceLevelObjectiveTimeWindowRolling", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveTimeWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelObjectiveTimeWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelObjectiveTimeWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b7f9bee90c8b0ffff04a770264055efe9e50a3b5f6b2e7571f2a8348dbe514e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRolling")
    def put_rolling(self, *, count: jsii.Number, unit: builtins.str) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#count ServiceLevel#count}.
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#unit ServiceLevel#unit}.
        '''
        value = ServiceLevelObjectiveTimeWindowRolling(count=count, unit=unit)

        return typing.cast(None, jsii.invoke(self, "putRolling", [value]))

    @builtins.property
    @jsii.member(jsii_name="rolling")
    def rolling(self) -> "ServiceLevelObjectiveTimeWindowRollingOutputReference":
        return typing.cast("ServiceLevelObjectiveTimeWindowRollingOutputReference", jsii.get(self, "rolling"))

    @builtins.property
    @jsii.member(jsii_name="rollingInput")
    def rolling_input(
        self,
    ) -> typing.Optional["ServiceLevelObjectiveTimeWindowRolling"]:
        return typing.cast(typing.Optional["ServiceLevelObjectiveTimeWindowRolling"], jsii.get(self, "rollingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceLevelObjectiveTimeWindow]:
        return typing.cast(typing.Optional[ServiceLevelObjectiveTimeWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelObjectiveTimeWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4391e2df40acf73b8012e83a32e62993c30b4417782ce77f7e084a13302f768d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelObjectiveTimeWindowRolling",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "unit": "unit"},
)
class ServiceLevelObjectiveTimeWindowRolling:
    def __init__(self, *, count: jsii.Number, unit: builtins.str) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#count ServiceLevel#count}.
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#unit ServiceLevel#unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__629bbbebd0b001dc8465f05a38be0a40c6554b2affce099f207d0316e33d5228)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "unit": unit,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#count ServiceLevel#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/service_level#unit ServiceLevel#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveTimeWindowRolling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelObjectiveTimeWindowRollingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.serviceLevel.ServiceLevelObjectiveTimeWindowRollingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__406a67e47cee09008e4484b12c6d11d9d19b171d8943683142851bfae3b61937)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a490b454ae9791ebf93e12f27dd8d4c8defa059455f776ae9c770916065fffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8267320c7a46f0504f6e64fee1eba4c254d16e10b1c178c7244ef4fde0d58946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceLevelObjectiveTimeWindowRolling]:
        return typing.cast(typing.Optional[ServiceLevelObjectiveTimeWindowRolling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelObjectiveTimeWindowRolling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d491976a9c1325934ccfea51f4d9b5376f96d2349039c50ec2a1b5e3dec9b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ServiceLevel",
    "ServiceLevelConfig",
    "ServiceLevelEvents",
    "ServiceLevelEventsBadEvents",
    "ServiceLevelEventsBadEventsOutputReference",
    "ServiceLevelEventsBadEventsSelect",
    "ServiceLevelEventsBadEventsSelectOutputReference",
    "ServiceLevelEventsGoodEvents",
    "ServiceLevelEventsGoodEventsOutputReference",
    "ServiceLevelEventsGoodEventsSelect",
    "ServiceLevelEventsGoodEventsSelectOutputReference",
    "ServiceLevelEventsOutputReference",
    "ServiceLevelEventsValidEvents",
    "ServiceLevelEventsValidEventsOutputReference",
    "ServiceLevelEventsValidEventsSelect",
    "ServiceLevelEventsValidEventsSelectOutputReference",
    "ServiceLevelObjective",
    "ServiceLevelObjectiveOutputReference",
    "ServiceLevelObjectiveTimeWindow",
    "ServiceLevelObjectiveTimeWindowOutputReference",
    "ServiceLevelObjectiveTimeWindowRolling",
    "ServiceLevelObjectiveTimeWindowRollingOutputReference",
]

publication.publish()

def _typecheckingstub__63476dcca6c12f410fba2b0b58d3d61fe6cbc24e408f95e1b9dde2ddd7e67c67(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    events: typing.Union[ServiceLevelEvents, typing.Dict[builtins.str, typing.Any]],
    guid: builtins.str,
    name: builtins.str,
    objective: typing.Union[ServiceLevelObjective, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__6e7de8ade568706777fbebda389d8fe73913d16787c3f3bdfb0575edd968f82b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac466664e39127beccf9d6af6a4cc30f505a249c590e63ca7f96d34ee1c0718c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40f4e4220646a5b5fef08ab8f99c77697b5087dbf384126dc53ff6445bd7fc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2429fe236c8a7c4ff13391b9f8d7bea17dd67c7553bb35b0d0e8b51afc9e0203(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a7d682edabbb1c0ac985154cad8e50335063f7f82d487714c6bc6a05b8b81d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed11a849c998def40d353dbdc59c1ee4ba95fde523da099f71fee6082e487e81(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    events: typing.Union[ServiceLevelEvents, typing.Dict[builtins.str, typing.Any]],
    guid: builtins.str,
    name: builtins.str,
    objective: typing.Union[ServiceLevelObjective, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16fed349c47b4dc9012248f526f151b88047a6790b6ac488a42c7c4f94ba7745(
    *,
    account_id: jsii.Number,
    valid_events: typing.Union[ServiceLevelEventsValidEvents, typing.Dict[builtins.str, typing.Any]],
    bad_events: typing.Optional[typing.Union[ServiceLevelEventsBadEvents, typing.Dict[builtins.str, typing.Any]]] = None,
    good_events: typing.Optional[typing.Union[ServiceLevelEventsGoodEvents, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f226aa354f3da3854346667fa02ef1c67a79d11e900658730768f01ad263d21c(
    *,
    from_: builtins.str,
    select: typing.Optional[typing.Union[ServiceLevelEventsBadEventsSelect, typing.Dict[builtins.str, typing.Any]]] = None,
    where: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e2e63bd7d50f86c87d54beb25cc6183ea39af4dd4ee0cb2a291206dd46cc35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb0a6f6ac73e8d0b838cb95b68849bcb097c5eabc1d9af015c4fca6e790037d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d51f376d840e0627e6e8dd4b0328da059b3eaa0bcdef57d8a0ccf72e823fef2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec85e29b5404c0795d92547d079dc047365547290c074a9005dffc6a3f306459(
    value: typing.Optional[ServiceLevelEventsBadEvents],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3e010a766d974590ea8e3dacb90a49454df4697492aef625be94a9aee8480b(
    *,
    function: builtins.str,
    attribute: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6beb9977fb9622f65253797306f9ed0e3cd81473577c4d8f2f54f2f85e284988(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0465fc92ef0f69f84ae296bb94516b73aa2b59690507103f09d332c7a63375d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4b39553c930810137eb3b3a8300272fca4890880c2f11f908cf9bdcd71fa9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756ac5be4115d542855924f63b231e3e52bfe71910f192345e26a8355fcc74a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246b07d89b1820dda9947a0fbe6e9c8d3f365a21f8c2840855ae41cd6c6f4856(
    value: typing.Optional[ServiceLevelEventsBadEventsSelect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8edabd1d65671aa6bc294c76b7daf127f10140766bdc36cbe19ed65086200db(
    *,
    from_: builtins.str,
    select: typing.Optional[typing.Union[ServiceLevelEventsGoodEventsSelect, typing.Dict[builtins.str, typing.Any]]] = None,
    where: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9c796b90359b55f12bf99e014b8b5a228572551e2890f6cb5b32153863c28f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a354f46ff97d5bf4afad9e63c8dae936e22d172b5405d7571364910bda3c4764(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2b8254a60421e9bcd0c4fef98c003953ec81d7d64ea157592d72af91839f34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20dbf8dc10e5608af9100bdb782df97647afbf7cbc1124f413d53a0b62383bb4(
    value: typing.Optional[ServiceLevelEventsGoodEvents],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff02bfd1a99e9d43dcfbf7e9d76999cde19b73b2db1c9cb6ef70c0e369bbf8e(
    *,
    function: builtins.str,
    attribute: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f65a7a475cfd972e95d57c0f06a465a45bdb957446e2dd3f1510773ab7dc3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219d9d577de36c6f38f06f665d5b4488c1203ae62385c403b020b33fe5f47a96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b755953a95d0a397515b959b74b0486396fbadaafada28ee90bd325a7df69cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc1e82e6bb33542cdb189499bad935419dda5aa6ca5011315ebc97eca2472c8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721b1f4b1ff43b5d56894e35e6f4539ef47633248bcbb711003adbb80e6bef48(
    value: typing.Optional[ServiceLevelEventsGoodEventsSelect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46355e76deb8bf790af2ecf7ac778e19cf9cee75bb5a37c18bb80cbe2d5d1fde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1e064b91227f92ac1b485c1fa277541096bf53b2ff2e49ea558f2d0859d3b8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a847dbaba7e277a0fb6e2309bffe18fcc937a86eabce205ac72407ff78de5086(
    value: typing.Optional[ServiceLevelEvents],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90407512972bcdfbae50767b5387f1ed11aaa209e379e9481f2347b7417deca(
    *,
    from_: builtins.str,
    select: typing.Optional[typing.Union[ServiceLevelEventsValidEventsSelect, typing.Dict[builtins.str, typing.Any]]] = None,
    where: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea711e534ff2dcae7d7dbd0bbcd5e501fe3c0e1b6b703891b18004858b04c90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025ea098b1da9ea8ce7d80550aa388f4bf397de373a318ab4d0c8d52914f4cc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ba5a112db8ced0bd89c7418c1872c4d42c486847558ee7de4c43e27c742e7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa67762b0cb32a0ee67195fc595ae7891bc29ca23b8213a7f628b5dd95a38683(
    value: typing.Optional[ServiceLevelEventsValidEvents],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31ae9ce08b6b6caf50215fa131116d277a209612270b24dbceb23651d8e2516(
    *,
    function: builtins.str,
    attribute: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51bbe89d925c41a9b1e7dd0a29651f62ce4b70e1f554e45585857bc205f7317(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f84f6d66d78947c88e9de4553108c51dff4a7d83d5730fb77b38748e953bbfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa354278f58cb1bc2a4949aedc55c12a835298364c7c8f283b8a89154342160(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df0a8af3dee4ba5ba2373b94fca9ee488848eacdd55f381370749dc5ae9f013(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfcab24df28d6ae5a0aeaec4d785387063a8690de64a0db80646dabe58313e43(
    value: typing.Optional[ServiceLevelEventsValidEventsSelect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2129b23dca73e5824bc883ec99252463b54fa6b8812b670f9cd30124eb3e6504(
    *,
    target: jsii.Number,
    time_window: typing.Union[ServiceLevelObjectiveTimeWindow, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0565ff2ab7edcc1ee366052c48b4a207a3fb50bd4ba2aa90f28e99f271cab8cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f4592414356bf5e2f2a0fea8b85441d7f481db57718b7c9ec15334071c0048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abba432439a67e09a322260e848c83deea2b1f44d45900d2558953a5162c182(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96e756a503d032985a4a344e4d9dc174bed038b04403bf612f2248cee114aaa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7243cb0c0f84b95ebbcc3e72e4ec5addbfdddd6bfd2709f303f737a9ef036e9c(
    value: typing.Optional[ServiceLevelObjective],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034692e62689dd89d0d545f4a280fe4bc97241633123180463f446ab69c660d6(
    *,
    rolling: typing.Union[ServiceLevelObjectiveTimeWindowRolling, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7f9bee90c8b0ffff04a770264055efe9e50a3b5f6b2e7571f2a8348dbe514e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4391e2df40acf73b8012e83a32e62993c30b4417782ce77f7e084a13302f768d(
    value: typing.Optional[ServiceLevelObjectiveTimeWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629bbbebd0b001dc8465f05a38be0a40c6554b2affce099f207d0316e33d5228(
    *,
    count: jsii.Number,
    unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__406a67e47cee09008e4484b12c6d11d9d19b171d8943683142851bfae3b61937(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a490b454ae9791ebf93e12f27dd8d4c8defa059455f776ae9c770916065fffa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8267320c7a46f0504f6e64fee1eba4c254d16e10b1c178c7244ef4fde0d58946(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d491976a9c1325934ccfea51f4d9b5376f96d2349039c50ec2a1b5e3dec9b96(
    value: typing.Optional[ServiceLevelObjectiveTimeWindowRolling],
) -> None:
    """Type checking stubs"""
    pass
