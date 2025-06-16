r'''
# `google_chronicle_watchlist`

Refer to the Terraform Registry for docs: [`google_chronicle_watchlist`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist).
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


class GoogleChronicleWatchlist(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleWatchlist.GoogleChronicleWatchlist",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist google_chronicle_watchlist}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        entity_population_mechanism: typing.Union["GoogleChronicleWatchlistEntityPopulationMechanism", typing.Dict[builtins.str, typing.Any]],
        instance: builtins.str,
        location: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        multiplying_factor: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleChronicleWatchlistTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        watchlist_id: typing.Optional[builtins.str] = None,
        watchlist_user_preferences: typing.Optional[typing.Union["GoogleChronicleWatchlistWatchlistUserPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist google_chronicle_watchlist} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Required. Display name of the watchlist. Note that it must be at least one character and less than 63 characters (https://google.aip.dev/148). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#display_name GoogleChronicleWatchlist#display_name}
        :param entity_population_mechanism: entity_population_mechanism block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#entity_population_mechanism GoogleChronicleWatchlist#entity_population_mechanism}
        :param instance: The unique identifier for the Chronicle instance, which is the same as the customer ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#instance GoogleChronicleWatchlist#instance}
        :param location: The location of the resource. This is the geographical region where the Chronicle instance resides, such as "us" or "europe-west2". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#location GoogleChronicleWatchlist#location}
        :param description: Optional. Description of the watchlist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#description GoogleChronicleWatchlist#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#id GoogleChronicleWatchlist#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param multiplying_factor: Optional. Weight applied to the risk score for entities in this watchlist. The default is 1.0 if it is not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#multiplying_factor GoogleChronicleWatchlist#multiplying_factor}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#project GoogleChronicleWatchlist#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#timeouts GoogleChronicleWatchlist#timeouts}
        :param watchlist_id: Optional. The ID to use for the watchlist, which will become the final component of the watchlist's resource name. This value should be 4-63 characters, and valid characters are /a-z-/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#watchlist_id GoogleChronicleWatchlist#watchlist_id}
        :param watchlist_user_preferences: watchlist_user_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#watchlist_user_preferences GoogleChronicleWatchlist#watchlist_user_preferences}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b47df3e891101937a88614cde54aa982b35199b0d8e0e3344ff42886e3264ed0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleChronicleWatchlistConfig(
            display_name=display_name,
            entity_population_mechanism=entity_population_mechanism,
            instance=instance,
            location=location,
            description=description,
            id=id,
            multiplying_factor=multiplying_factor,
            project=project,
            timeouts=timeouts,
            watchlist_id=watchlist_id,
            watchlist_user_preferences=watchlist_user_preferences,
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
        '''Generates CDKTF code for importing a GoogleChronicleWatchlist resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleChronicleWatchlist to import.
        :param import_from_id: The id of the existing GoogleChronicleWatchlist that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleChronicleWatchlist to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ec63625b6ba6a9aa3886737a85052243744ad39cf32e48a3191c4532acb7a4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEntityPopulationMechanism")
    def put_entity_population_mechanism(
        self,
        *,
        manual: typing.Optional[typing.Union["GoogleChronicleWatchlistEntityPopulationMechanismManual", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param manual: manual block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#manual GoogleChronicleWatchlist#manual}
        '''
        value = GoogleChronicleWatchlistEntityPopulationMechanism(manual=manual)

        return typing.cast(None, jsii.invoke(self, "putEntityPopulationMechanism", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#create GoogleChronicleWatchlist#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#delete GoogleChronicleWatchlist#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#update GoogleChronicleWatchlist#update}.
        '''
        value = GoogleChronicleWatchlistTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWatchlistUserPreferences")
    def put_watchlist_user_preferences(
        self,
        *,
        pinned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pinned: Optional. Whether the watchlist is pinned on the dashboard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#pinned GoogleChronicleWatchlist#pinned}
        '''
        value = GoogleChronicleWatchlistWatchlistUserPreferences(pinned=pinned)

        return typing.cast(None, jsii.invoke(self, "putWatchlistUserPreferences", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMultiplyingFactor")
    def reset_multiplying_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiplyingFactor", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWatchlistId")
    def reset_watchlist_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWatchlistId", []))

    @jsii.member(jsii_name="resetWatchlistUserPreferences")
    def reset_watchlist_user_preferences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWatchlistUserPreferences", []))

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
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="entityCount")
    def entity_count(self) -> "GoogleChronicleWatchlistEntityCountList":
        return typing.cast("GoogleChronicleWatchlistEntityCountList", jsii.get(self, "entityCount"))

    @builtins.property
    @jsii.member(jsii_name="entityPopulationMechanism")
    def entity_population_mechanism(
        self,
    ) -> "GoogleChronicleWatchlistEntityPopulationMechanismOutputReference":
        return typing.cast("GoogleChronicleWatchlistEntityPopulationMechanismOutputReference", jsii.get(self, "entityPopulationMechanism"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleChronicleWatchlistTimeoutsOutputReference":
        return typing.cast("GoogleChronicleWatchlistTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="watchlistUserPreferences")
    def watchlist_user_preferences(
        self,
    ) -> "GoogleChronicleWatchlistWatchlistUserPreferencesOutputReference":
        return typing.cast("GoogleChronicleWatchlistWatchlistUserPreferencesOutputReference", jsii.get(self, "watchlistUserPreferences"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="entityPopulationMechanismInput")
    def entity_population_mechanism_input(
        self,
    ) -> typing.Optional["GoogleChronicleWatchlistEntityPopulationMechanism"]:
        return typing.cast(typing.Optional["GoogleChronicleWatchlistEntityPopulationMechanism"], jsii.get(self, "entityPopulationMechanismInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="multiplyingFactorInput")
    def multiplying_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "multiplyingFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleChronicleWatchlistTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleChronicleWatchlistTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="watchlistIdInput")
    def watchlist_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "watchlistIdInput"))

    @builtins.property
    @jsii.member(jsii_name="watchlistUserPreferencesInput")
    def watchlist_user_preferences_input(
        self,
    ) -> typing.Optional["GoogleChronicleWatchlistWatchlistUserPreferences"]:
        return typing.cast(typing.Optional["GoogleChronicleWatchlistWatchlistUserPreferences"], jsii.get(self, "watchlistUserPreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef67095152ceb2f22851b70751c708dfabfceb22c91b69eceabf9ce0423ed1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db557eeadbacb1100afce6a7850befe1c86a951c8e74c7e3f9f3b84c358e87d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0974aaed4f0140c7ca10be3d6f33934e40ba93d47273ca6a4c4c4d140a2e209b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e98550131ff32f5e1fed90529ef0a7172e3afc22d2cbc6abe40fa683dd4344f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f092a4852eba225ec536d8f3c7dd9f6c68f0261109ab1bed0b5511b7eb2bcf74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiplyingFactor")
    def multiplying_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "multiplyingFactor"))

    @multiplying_factor.setter
    def multiplying_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b909c9ec0f656834a585edbdc00169208ec527c1eb790d35466e6230a0b125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiplyingFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8282053653ca05286bfd84bcbb4b59be12df15b6b30d717fe1c8953c7980cca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="watchlistId")
    def watchlist_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "watchlistId"))

    @watchlist_id.setter
    def watchlist_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9feca580dbbe296ca257089211fa4143b1e22c1916184cd334b4057ec3366c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "watchlistId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleChronicleWatchlist.GoogleChronicleWatchlistConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "entity_population_mechanism": "entityPopulationMechanism",
        "instance": "instance",
        "location": "location",
        "description": "description",
        "id": "id",
        "multiplying_factor": "multiplyingFactor",
        "project": "project",
        "timeouts": "timeouts",
        "watchlist_id": "watchlistId",
        "watchlist_user_preferences": "watchlistUserPreferences",
    },
)
class GoogleChronicleWatchlistConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        entity_population_mechanism: typing.Union["GoogleChronicleWatchlistEntityPopulationMechanism", typing.Dict[builtins.str, typing.Any]],
        instance: builtins.str,
        location: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        multiplying_factor: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleChronicleWatchlistTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        watchlist_id: typing.Optional[builtins.str] = None,
        watchlist_user_preferences: typing.Optional[typing.Union["GoogleChronicleWatchlistWatchlistUserPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Required. Display name of the watchlist. Note that it must be at least one character and less than 63 characters (https://google.aip.dev/148). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#display_name GoogleChronicleWatchlist#display_name}
        :param entity_population_mechanism: entity_population_mechanism block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#entity_population_mechanism GoogleChronicleWatchlist#entity_population_mechanism}
        :param instance: The unique identifier for the Chronicle instance, which is the same as the customer ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#instance GoogleChronicleWatchlist#instance}
        :param location: The location of the resource. This is the geographical region where the Chronicle instance resides, such as "us" or "europe-west2". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#location GoogleChronicleWatchlist#location}
        :param description: Optional. Description of the watchlist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#description GoogleChronicleWatchlist#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#id GoogleChronicleWatchlist#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param multiplying_factor: Optional. Weight applied to the risk score for entities in this watchlist. The default is 1.0 if it is not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#multiplying_factor GoogleChronicleWatchlist#multiplying_factor}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#project GoogleChronicleWatchlist#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#timeouts GoogleChronicleWatchlist#timeouts}
        :param watchlist_id: Optional. The ID to use for the watchlist, which will become the final component of the watchlist's resource name. This value should be 4-63 characters, and valid characters are /a-z-/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#watchlist_id GoogleChronicleWatchlist#watchlist_id}
        :param watchlist_user_preferences: watchlist_user_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#watchlist_user_preferences GoogleChronicleWatchlist#watchlist_user_preferences}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(entity_population_mechanism, dict):
            entity_population_mechanism = GoogleChronicleWatchlistEntityPopulationMechanism(**entity_population_mechanism)
        if isinstance(timeouts, dict):
            timeouts = GoogleChronicleWatchlistTimeouts(**timeouts)
        if isinstance(watchlist_user_preferences, dict):
            watchlist_user_preferences = GoogleChronicleWatchlistWatchlistUserPreferences(**watchlist_user_preferences)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5e2b4b1749ac207f8102232a8f43ff8b5bfe4090cb0c9b0393dd6a24f379e8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument entity_population_mechanism", value=entity_population_mechanism, expected_type=type_hints["entity_population_mechanism"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument multiplying_factor", value=multiplying_factor, expected_type=type_hints["multiplying_factor"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument watchlist_id", value=watchlist_id, expected_type=type_hints["watchlist_id"])
            check_type(argname="argument watchlist_user_preferences", value=watchlist_user_preferences, expected_type=type_hints["watchlist_user_preferences"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "entity_population_mechanism": entity_population_mechanism,
            "instance": instance,
            "location": location,
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
        if multiplying_factor is not None:
            self._values["multiplying_factor"] = multiplying_factor
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if watchlist_id is not None:
            self._values["watchlist_id"] = watchlist_id
        if watchlist_user_preferences is not None:
            self._values["watchlist_user_preferences"] = watchlist_user_preferences

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
    def display_name(self) -> builtins.str:
        '''Required. Display name of the watchlist. Note that it must be at least one character and less than 63 characters (https://google.aip.dev/148).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#display_name GoogleChronicleWatchlist#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entity_population_mechanism(
        self,
    ) -> "GoogleChronicleWatchlistEntityPopulationMechanism":
        '''entity_population_mechanism block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#entity_population_mechanism GoogleChronicleWatchlist#entity_population_mechanism}
        '''
        result = self._values.get("entity_population_mechanism")
        assert result is not None, "Required property 'entity_population_mechanism' is missing"
        return typing.cast("GoogleChronicleWatchlistEntityPopulationMechanism", result)

    @builtins.property
    def instance(self) -> builtins.str:
        '''The unique identifier for the Chronicle instance, which is the same as the customer ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#instance GoogleChronicleWatchlist#instance}
        '''
        result = self._values.get("instance")
        assert result is not None, "Required property 'instance' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        This is the geographical region where the Chronicle instance resides, such as "us" or "europe-west2".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#location GoogleChronicleWatchlist#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the watchlist.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#description GoogleChronicleWatchlist#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#id GoogleChronicleWatchlist#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multiplying_factor(self) -> typing.Optional[jsii.Number]:
        '''Optional. Weight applied to the risk score for entities in this watchlist. The default is 1.0 if it is not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#multiplying_factor GoogleChronicleWatchlist#multiplying_factor}
        '''
        result = self._values.get("multiplying_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#project GoogleChronicleWatchlist#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleChronicleWatchlistTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#timeouts GoogleChronicleWatchlist#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleChronicleWatchlistTimeouts"], result)

    @builtins.property
    def watchlist_id(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The ID to use for the watchlist,
        which will become the final component of the watchlist's resource name.
        This value should be 4-63 characters, and valid characters
        are /a-z-/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#watchlist_id GoogleChronicleWatchlist#watchlist_id}
        '''
        result = self._values.get("watchlist_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def watchlist_user_preferences(
        self,
    ) -> typing.Optional["GoogleChronicleWatchlistWatchlistUserPreferences"]:
        '''watchlist_user_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#watchlist_user_preferences GoogleChronicleWatchlist#watchlist_user_preferences}
        '''
        result = self._values.get("watchlist_user_preferences")
        return typing.cast(typing.Optional["GoogleChronicleWatchlistWatchlistUserPreferences"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleChronicleWatchlistConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleChronicleWatchlist.GoogleChronicleWatchlistEntityCount",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleChronicleWatchlistEntityCount:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleChronicleWatchlistEntityCount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleChronicleWatchlistEntityCountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleWatchlist.GoogleChronicleWatchlistEntityCountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1e31416540545b4259b4dcd4f6a9292029cc05ba2faff6a088a4d3eb39b3b1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleChronicleWatchlistEntityCountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed77c253202c7d85b647c32071a033220de29fab9fb84601cf97d9ad695da94)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleChronicleWatchlistEntityCountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a20984db47e9b39f2a0cc35be2b5d5faf74c2240bb1e821d9f0deefa93c3d293)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09417681c4b150fe4841f0cecedd42c06aa56178c2ae1b4f7c2f8d2302bacf71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ead15a97a0ef6414253d3ce4f7946f04986602d92ca48bafd848d31fdef3a9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleChronicleWatchlistEntityCountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleWatchlist.GoogleChronicleWatchlistEntityCountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcca65ca295c8ed40d59a2c75ef89b43d86a7aff789ab655cba59f1bcd3752d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="asset")
    def asset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "asset"))

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "user"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleChronicleWatchlistEntityCount]:
        return typing.cast(typing.Optional[GoogleChronicleWatchlistEntityCount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleChronicleWatchlistEntityCount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a265fdcbf805227fece7d17dbbee50a0600799910586063b7eedd8d087a0b0fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleChronicleWatchlist.GoogleChronicleWatchlistEntityPopulationMechanism",
    jsii_struct_bases=[],
    name_mapping={"manual": "manual"},
)
class GoogleChronicleWatchlistEntityPopulationMechanism:
    def __init__(
        self,
        *,
        manual: typing.Optional[typing.Union["GoogleChronicleWatchlistEntityPopulationMechanismManual", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param manual: manual block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#manual GoogleChronicleWatchlist#manual}
        '''
        if isinstance(manual, dict):
            manual = GoogleChronicleWatchlistEntityPopulationMechanismManual(**manual)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de5f6f550eac8c7bc080258d3106ae69725a87bc61fa970e7748b6b6825fc0dc)
            check_type(argname="argument manual", value=manual, expected_type=type_hints["manual"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if manual is not None:
            self._values["manual"] = manual

    @builtins.property
    def manual(
        self,
    ) -> typing.Optional["GoogleChronicleWatchlistEntityPopulationMechanismManual"]:
        '''manual block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#manual GoogleChronicleWatchlist#manual}
        '''
        result = self._values.get("manual")
        return typing.cast(typing.Optional["GoogleChronicleWatchlistEntityPopulationMechanismManual"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleChronicleWatchlistEntityPopulationMechanism(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleChronicleWatchlist.GoogleChronicleWatchlistEntityPopulationMechanismManual",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleChronicleWatchlistEntityPopulationMechanismManual:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleChronicleWatchlistEntityPopulationMechanismManual(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleChronicleWatchlistEntityPopulationMechanismManualOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleWatchlist.GoogleChronicleWatchlistEntityPopulationMechanismManualOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__726da7e1274572ee2059ecec469ff4ee7fd1b48545d58afbeb865a6f30da374e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleChronicleWatchlistEntityPopulationMechanismManual]:
        return typing.cast(typing.Optional[GoogleChronicleWatchlistEntityPopulationMechanismManual], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleChronicleWatchlistEntityPopulationMechanismManual],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1522712b95f99f7419a140a84d7a6f39d74db6a979e1415357234d576babd981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleChronicleWatchlistEntityPopulationMechanismOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleWatchlist.GoogleChronicleWatchlistEntityPopulationMechanismOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__078f07b031b53ef148dfdfd47f44844f7dcc8fea4016c0c83808e2af9dee9e09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putManual")
    def put_manual(self) -> None:
        value = GoogleChronicleWatchlistEntityPopulationMechanismManual()

        return typing.cast(None, jsii.invoke(self, "putManual", [value]))

    @jsii.member(jsii_name="resetManual")
    def reset_manual(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManual", []))

    @builtins.property
    @jsii.member(jsii_name="manual")
    def manual(
        self,
    ) -> GoogleChronicleWatchlistEntityPopulationMechanismManualOutputReference:
        return typing.cast(GoogleChronicleWatchlistEntityPopulationMechanismManualOutputReference, jsii.get(self, "manual"))

    @builtins.property
    @jsii.member(jsii_name="manualInput")
    def manual_input(
        self,
    ) -> typing.Optional[GoogleChronicleWatchlistEntityPopulationMechanismManual]:
        return typing.cast(typing.Optional[GoogleChronicleWatchlistEntityPopulationMechanismManual], jsii.get(self, "manualInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleChronicleWatchlistEntityPopulationMechanism]:
        return typing.cast(typing.Optional[GoogleChronicleWatchlistEntityPopulationMechanism], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleChronicleWatchlistEntityPopulationMechanism],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac03bff8b1a50cc307dd19cbca381e408bb0d07d0e5b101fb55238f52454c36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleChronicleWatchlist.GoogleChronicleWatchlistTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleChronicleWatchlistTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#create GoogleChronicleWatchlist#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#delete GoogleChronicleWatchlist#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#update GoogleChronicleWatchlist#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f0f11c36068cc42baf433b6c579fbb1b43e4692fef2df7cdcb3cb5c655650b)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#create GoogleChronicleWatchlist#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#delete GoogleChronicleWatchlist#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#update GoogleChronicleWatchlist#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleChronicleWatchlistTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleChronicleWatchlistTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleWatchlist.GoogleChronicleWatchlistTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69afab5ff688e002d94e2b0adc17a7a8cbd085a3909d3149d276e7fa06f67154)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__51e6237dafbb18d103f9e05f937692ce3af51d5e53c2ee649c0b5dc0a71722b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7543fbf8fb790b87aa110dbcd7e03f5490cf75a22d4b7d05ec0992ffe4e1399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91dbe1f79e3630c542bfe4e99074d8049fc85c2ac3ac2def852ae1e0a11f268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleWatchlistTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleWatchlistTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleWatchlistTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00720c2cf48810761845019ebdedb17cd5915c0f8d1317e1e17ecded4b6ce5b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleChronicleWatchlist.GoogleChronicleWatchlistWatchlistUserPreferences",
    jsii_struct_bases=[],
    name_mapping={"pinned": "pinned"},
)
class GoogleChronicleWatchlistWatchlistUserPreferences:
    def __init__(
        self,
        *,
        pinned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pinned: Optional. Whether the watchlist is pinned on the dashboard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#pinned GoogleChronicleWatchlist#pinned}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b54677af35206cd3f749c7f1194b7ef6bc53b266d5a1cc1dd0254df6b71d3e)
            check_type(argname="argument pinned", value=pinned, expected_type=type_hints["pinned"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pinned is not None:
            self._values["pinned"] = pinned

    @builtins.property
    def pinned(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Whether the watchlist is pinned on the dashboard.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_watchlist#pinned GoogleChronicleWatchlist#pinned}
        '''
        result = self._values.get("pinned")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleChronicleWatchlistWatchlistUserPreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleChronicleWatchlistWatchlistUserPreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleWatchlist.GoogleChronicleWatchlistWatchlistUserPreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ab5369842b20375673aa955f40539f434deb27e5574ae4d9f9e65d4596c44b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPinned")
    def reset_pinned(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPinned", []))

    @builtins.property
    @jsii.member(jsii_name="pinnedInput")
    def pinned_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pinnedInput"))

    @builtins.property
    @jsii.member(jsii_name="pinned")
    def pinned(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pinned"))

    @pinned.setter
    def pinned(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__720b1c4da37a42f23953a5717bf737dba9bd60ed7d1aa81cae4b9a47c69ea34b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pinned", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleChronicleWatchlistWatchlistUserPreferences]:
        return typing.cast(typing.Optional[GoogleChronicleWatchlistWatchlistUserPreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleChronicleWatchlistWatchlistUserPreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04b3f3b85290583f0d3a668216b7dd0bd25f7123dbd1ff40dbcee7cd4b884b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleChronicleWatchlist",
    "GoogleChronicleWatchlistConfig",
    "GoogleChronicleWatchlistEntityCount",
    "GoogleChronicleWatchlistEntityCountList",
    "GoogleChronicleWatchlistEntityCountOutputReference",
    "GoogleChronicleWatchlistEntityPopulationMechanism",
    "GoogleChronicleWatchlistEntityPopulationMechanismManual",
    "GoogleChronicleWatchlistEntityPopulationMechanismManualOutputReference",
    "GoogleChronicleWatchlistEntityPopulationMechanismOutputReference",
    "GoogleChronicleWatchlistTimeouts",
    "GoogleChronicleWatchlistTimeoutsOutputReference",
    "GoogleChronicleWatchlistWatchlistUserPreferences",
    "GoogleChronicleWatchlistWatchlistUserPreferencesOutputReference",
]

publication.publish()

def _typecheckingstub__b47df3e891101937a88614cde54aa982b35199b0d8e0e3344ff42886e3264ed0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    entity_population_mechanism: typing.Union[GoogleChronicleWatchlistEntityPopulationMechanism, typing.Dict[builtins.str, typing.Any]],
    instance: builtins.str,
    location: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    multiplying_factor: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleChronicleWatchlistTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    watchlist_id: typing.Optional[builtins.str] = None,
    watchlist_user_preferences: typing.Optional[typing.Union[GoogleChronicleWatchlistWatchlistUserPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__76ec63625b6ba6a9aa3886737a85052243744ad39cf32e48a3191c4532acb7a4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef67095152ceb2f22851b70751c708dfabfceb22c91b69eceabf9ce0423ed1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db557eeadbacb1100afce6a7850befe1c86a951c8e74c7e3f9f3b84c358e87d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0974aaed4f0140c7ca10be3d6f33934e40ba93d47273ca6a4c4c4d140a2e209b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e98550131ff32f5e1fed90529ef0a7172e3afc22d2cbc6abe40fa683dd4344f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f092a4852eba225ec536d8f3c7dd9f6c68f0261109ab1bed0b5511b7eb2bcf74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b909c9ec0f656834a585edbdc00169208ec527c1eb790d35466e6230a0b125(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8282053653ca05286bfd84bcbb4b59be12df15b6b30d717fe1c8953c7980cca9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9feca580dbbe296ca257089211fa4143b1e22c1916184cd334b4057ec3366c86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5e2b4b1749ac207f8102232a8f43ff8b5bfe4090cb0c9b0393dd6a24f379e8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    entity_population_mechanism: typing.Union[GoogleChronicleWatchlistEntityPopulationMechanism, typing.Dict[builtins.str, typing.Any]],
    instance: builtins.str,
    location: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    multiplying_factor: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleChronicleWatchlistTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    watchlist_id: typing.Optional[builtins.str] = None,
    watchlist_user_preferences: typing.Optional[typing.Union[GoogleChronicleWatchlistWatchlistUserPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e31416540545b4259b4dcd4f6a9292029cc05ba2faff6a088a4d3eb39b3b1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed77c253202c7d85b647c32071a033220de29fab9fb84601cf97d9ad695da94(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20984db47e9b39f2a0cc35be2b5d5faf74c2240bb1e821d9f0deefa93c3d293(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09417681c4b150fe4841f0cecedd42c06aa56178c2ae1b4f7c2f8d2302bacf71(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ead15a97a0ef6414253d3ce4f7946f04986602d92ca48bafd848d31fdef3a9c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcca65ca295c8ed40d59a2c75ef89b43d86a7aff789ab655cba59f1bcd3752d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a265fdcbf805227fece7d17dbbee50a0600799910586063b7eedd8d087a0b0fc(
    value: typing.Optional[GoogleChronicleWatchlistEntityCount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5f6f550eac8c7bc080258d3106ae69725a87bc61fa970e7748b6b6825fc0dc(
    *,
    manual: typing.Optional[typing.Union[GoogleChronicleWatchlistEntityPopulationMechanismManual, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726da7e1274572ee2059ecec469ff4ee7fd1b48545d58afbeb865a6f30da374e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1522712b95f99f7419a140a84d7a6f39d74db6a979e1415357234d576babd981(
    value: typing.Optional[GoogleChronicleWatchlistEntityPopulationMechanismManual],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078f07b031b53ef148dfdfd47f44844f7dcc8fea4016c0c83808e2af9dee9e09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac03bff8b1a50cc307dd19cbca381e408bb0d07d0e5b101fb55238f52454c36(
    value: typing.Optional[GoogleChronicleWatchlistEntityPopulationMechanism],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f0f11c36068cc42baf433b6c579fbb1b43e4692fef2df7cdcb3cb5c655650b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69afab5ff688e002d94e2b0adc17a7a8cbd085a3909d3149d276e7fa06f67154(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e6237dafbb18d103f9e05f937692ce3af51d5e53c2ee649c0b5dc0a71722b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7543fbf8fb790b87aa110dbcd7e03f5490cf75a22d4b7d05ec0992ffe4e1399(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91dbe1f79e3630c542bfe4e99074d8049fc85c2ac3ac2def852ae1e0a11f268(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00720c2cf48810761845019ebdedb17cd5915c0f8d1317e1e17ecded4b6ce5b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleWatchlistTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b54677af35206cd3f749c7f1194b7ef6bc53b266d5a1cc1dd0254df6b71d3e(
    *,
    pinned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab5369842b20375673aa955f40539f434deb27e5574ae4d9f9e65d4596c44b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720b1c4da37a42f23953a5717bf737dba9bd60ed7d1aa81cae4b9a47c69ea34b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04b3f3b85290583f0d3a668216b7dd0bd25f7123dbd1ff40dbcee7cd4b884b6(
    value: typing.Optional[GoogleChronicleWatchlistWatchlistUserPreferences],
) -> None:
    """Type checking stubs"""
    pass
