r'''
# `google_chronicle_watchlist`

Refer to the Terraform Registry for docs: [`google_chronicle_watchlist`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist).
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


class ChronicleWatchlist(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleWatchlist.ChronicleWatchlist",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist google_chronicle_watchlist}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        entity_population_mechanism: typing.Union["ChronicleWatchlistEntityPopulationMechanism", typing.Dict[builtins.str, typing.Any]],
        instance: builtins.str,
        location: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        multiplying_factor: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ChronicleWatchlistTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        watchlist_id: typing.Optional[builtins.str] = None,
        watchlist_user_preferences: typing.Optional[typing.Union["ChronicleWatchlistWatchlistUserPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist google_chronicle_watchlist} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Required. Display name of the watchlist. Note that it must be at least one character and less than 63 characters (https://google.aip.dev/148). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#display_name ChronicleWatchlist#display_name}
        :param entity_population_mechanism: entity_population_mechanism block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#entity_population_mechanism ChronicleWatchlist#entity_population_mechanism}
        :param instance: The unique identifier for the Chronicle instance, which is the same as the customer ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#instance ChronicleWatchlist#instance}
        :param location: The location of the resource. This is the geographical region where the Chronicle instance resides, such as "us" or "europe-west2". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#location ChronicleWatchlist#location}
        :param description: Optional. Description of the watchlist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#description ChronicleWatchlist#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#id ChronicleWatchlist#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param multiplying_factor: Optional. Weight applied to the risk score for entities in this watchlist. The default is 1.0 if it is not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#multiplying_factor ChronicleWatchlist#multiplying_factor}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#project ChronicleWatchlist#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#timeouts ChronicleWatchlist#timeouts}
        :param watchlist_id: Optional. The ID to use for the watchlist, which will become the final component of the watchlist's resource name. This value should be 4-63 characters, and valid characters are /a-z-/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#watchlist_id ChronicleWatchlist#watchlist_id}
        :param watchlist_user_preferences: watchlist_user_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#watchlist_user_preferences ChronicleWatchlist#watchlist_user_preferences}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd90a5bea53bd637b39d0b0ecbeb4424a14970cf9c38e96b10b5ca507d931aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ChronicleWatchlistConfig(
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
        '''Generates CDKTF code for importing a ChronicleWatchlist resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ChronicleWatchlist to import.
        :param import_from_id: The id of the existing ChronicleWatchlist that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ChronicleWatchlist to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0278d9c37c0b84008a6414fe4de471050e30c39f0ae304360984148fcbc307fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEntityPopulationMechanism")
    def put_entity_population_mechanism(
        self,
        *,
        manual: typing.Optional[typing.Union["ChronicleWatchlistEntityPopulationMechanismManual", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param manual: manual block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#manual ChronicleWatchlist#manual}
        '''
        value = ChronicleWatchlistEntityPopulationMechanism(manual=manual)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#create ChronicleWatchlist#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#delete ChronicleWatchlist#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#update ChronicleWatchlist#update}.
        '''
        value = ChronicleWatchlistTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWatchlistUserPreferences")
    def put_watchlist_user_preferences(
        self,
        *,
        pinned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pinned: Optional. Whether the watchlist is pinned on the dashboard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#pinned ChronicleWatchlist#pinned}
        '''
        value = ChronicleWatchlistWatchlistUserPreferences(pinned=pinned)

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
    def entity_count(self) -> "ChronicleWatchlistEntityCountList":
        return typing.cast("ChronicleWatchlistEntityCountList", jsii.get(self, "entityCount"))

    @builtins.property
    @jsii.member(jsii_name="entityPopulationMechanism")
    def entity_population_mechanism(
        self,
    ) -> "ChronicleWatchlistEntityPopulationMechanismOutputReference":
        return typing.cast("ChronicleWatchlistEntityPopulationMechanismOutputReference", jsii.get(self, "entityPopulationMechanism"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ChronicleWatchlistTimeoutsOutputReference":
        return typing.cast("ChronicleWatchlistTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="watchlistUserPreferences")
    def watchlist_user_preferences(
        self,
    ) -> "ChronicleWatchlistWatchlistUserPreferencesOutputReference":
        return typing.cast("ChronicleWatchlistWatchlistUserPreferencesOutputReference", jsii.get(self, "watchlistUserPreferences"))

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
    ) -> typing.Optional["ChronicleWatchlistEntityPopulationMechanism"]:
        return typing.cast(typing.Optional["ChronicleWatchlistEntityPopulationMechanism"], jsii.get(self, "entityPopulationMechanismInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ChronicleWatchlistTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ChronicleWatchlistTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="watchlistIdInput")
    def watchlist_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "watchlistIdInput"))

    @builtins.property
    @jsii.member(jsii_name="watchlistUserPreferencesInput")
    def watchlist_user_preferences_input(
        self,
    ) -> typing.Optional["ChronicleWatchlistWatchlistUserPreferences"]:
        return typing.cast(typing.Optional["ChronicleWatchlistWatchlistUserPreferences"], jsii.get(self, "watchlistUserPreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3002ac90cadd9192f2a5aed40784cdc75d0934e2077ec05ae8c77dae2fa7fe59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5218b8cd574abe0d07139e4923c356def6f561a7483390055e8d20fa18c25214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e2a6180c5ae63bac4168b3077e82af562a28d8732e2541539a24be29c9f5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7916d00faaa1d00328366c363947beb9bc60ef876f4b29b54e8a722f00880c6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8505127ba0d798d56c432a09c732bf344951a48c46e00854729f52f3320e915b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiplyingFactor")
    def multiplying_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "multiplyingFactor"))

    @multiplying_factor.setter
    def multiplying_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e088f5dd99a618b70d0e0e706267946c5125935cc79f251f425036dba7ee8b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiplyingFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ef61f5c0355bbf14f136c383d859aa037160af21312b0c95cb716e00734191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="watchlistId")
    def watchlist_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "watchlistId"))

    @watchlist_id.setter
    def watchlist_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c610918e0b75e3347efeae7c74fb7d472cbbd5332dce157ca74d3508c03e0f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "watchlistId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.chronicleWatchlist.ChronicleWatchlistConfig",
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
class ChronicleWatchlistConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        entity_population_mechanism: typing.Union["ChronicleWatchlistEntityPopulationMechanism", typing.Dict[builtins.str, typing.Any]],
        instance: builtins.str,
        location: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        multiplying_factor: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ChronicleWatchlistTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        watchlist_id: typing.Optional[builtins.str] = None,
        watchlist_user_preferences: typing.Optional[typing.Union["ChronicleWatchlistWatchlistUserPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Required. Display name of the watchlist. Note that it must be at least one character and less than 63 characters (https://google.aip.dev/148). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#display_name ChronicleWatchlist#display_name}
        :param entity_population_mechanism: entity_population_mechanism block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#entity_population_mechanism ChronicleWatchlist#entity_population_mechanism}
        :param instance: The unique identifier for the Chronicle instance, which is the same as the customer ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#instance ChronicleWatchlist#instance}
        :param location: The location of the resource. This is the geographical region where the Chronicle instance resides, such as "us" or "europe-west2". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#location ChronicleWatchlist#location}
        :param description: Optional. Description of the watchlist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#description ChronicleWatchlist#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#id ChronicleWatchlist#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param multiplying_factor: Optional. Weight applied to the risk score for entities in this watchlist. The default is 1.0 if it is not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#multiplying_factor ChronicleWatchlist#multiplying_factor}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#project ChronicleWatchlist#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#timeouts ChronicleWatchlist#timeouts}
        :param watchlist_id: Optional. The ID to use for the watchlist, which will become the final component of the watchlist's resource name. This value should be 4-63 characters, and valid characters are /a-z-/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#watchlist_id ChronicleWatchlist#watchlist_id}
        :param watchlist_user_preferences: watchlist_user_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#watchlist_user_preferences ChronicleWatchlist#watchlist_user_preferences}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(entity_population_mechanism, dict):
            entity_population_mechanism = ChronicleWatchlistEntityPopulationMechanism(**entity_population_mechanism)
        if isinstance(timeouts, dict):
            timeouts = ChronicleWatchlistTimeouts(**timeouts)
        if isinstance(watchlist_user_preferences, dict):
            watchlist_user_preferences = ChronicleWatchlistWatchlistUserPreferences(**watchlist_user_preferences)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086d3265ae272408a8f928fe81ba72f73446ad2f9ed7159914defcbb5c285965)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#display_name ChronicleWatchlist#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entity_population_mechanism(
        self,
    ) -> "ChronicleWatchlistEntityPopulationMechanism":
        '''entity_population_mechanism block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#entity_population_mechanism ChronicleWatchlist#entity_population_mechanism}
        '''
        result = self._values.get("entity_population_mechanism")
        assert result is not None, "Required property 'entity_population_mechanism' is missing"
        return typing.cast("ChronicleWatchlistEntityPopulationMechanism", result)

    @builtins.property
    def instance(self) -> builtins.str:
        '''The unique identifier for the Chronicle instance, which is the same as the customer ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#instance ChronicleWatchlist#instance}
        '''
        result = self._values.get("instance")
        assert result is not None, "Required property 'instance' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        This is the geographical region where the Chronicle instance resides, such as "us" or "europe-west2".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#location ChronicleWatchlist#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the watchlist.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#description ChronicleWatchlist#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#id ChronicleWatchlist#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multiplying_factor(self) -> typing.Optional[jsii.Number]:
        '''Optional. Weight applied to the risk score for entities in this watchlist. The default is 1.0 if it is not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#multiplying_factor ChronicleWatchlist#multiplying_factor}
        '''
        result = self._values.get("multiplying_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#project ChronicleWatchlist#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ChronicleWatchlistTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#timeouts ChronicleWatchlist#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ChronicleWatchlistTimeouts"], result)

    @builtins.property
    def watchlist_id(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The ID to use for the watchlist,
        which will become the final component of the watchlist's resource name.
        This value should be 4-63 characters, and valid characters
        are /a-z-/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#watchlist_id ChronicleWatchlist#watchlist_id}
        '''
        result = self._values.get("watchlist_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def watchlist_user_preferences(
        self,
    ) -> typing.Optional["ChronicleWatchlistWatchlistUserPreferences"]:
        '''watchlist_user_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#watchlist_user_preferences ChronicleWatchlist#watchlist_user_preferences}
        '''
        result = self._values.get("watchlist_user_preferences")
        return typing.cast(typing.Optional["ChronicleWatchlistWatchlistUserPreferences"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChronicleWatchlistConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.chronicleWatchlist.ChronicleWatchlistEntityCount",
    jsii_struct_bases=[],
    name_mapping={},
)
class ChronicleWatchlistEntityCount:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChronicleWatchlistEntityCount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChronicleWatchlistEntityCountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleWatchlist.ChronicleWatchlistEntityCountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5836a192d080a5cf4f9e37fe41cf792b74001cfc58c7e465093bbe4f667f87e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ChronicleWatchlistEntityCountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f1d6dfb03f9b350eb78966a64d855beeff2f5c05d72f621dfbea9b08c44e0d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ChronicleWatchlistEntityCountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6095540d9905b9fcf029977feec71987080f68ae16e1278caeb7bc531f4cdf5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3abc3065078d023d2b0f0a0c8334c13ec78ff17075ba1b8e512726f063bf6c99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c30cfc2598cdc6f197dd4ad8ffa0b3adb064e45d2f27a0781849052fb90f643c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ChronicleWatchlistEntityCountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleWatchlist.ChronicleWatchlistEntityCountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0ab475238bbcd49c434abc6211757eb23be4de69b910c9c91f3e756237aa1e5)
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
    def internal_value(self) -> typing.Optional[ChronicleWatchlistEntityCount]:
        return typing.cast(typing.Optional[ChronicleWatchlistEntityCount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChronicleWatchlistEntityCount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c0c62358f168f532f86577ec4264467df7229a7ccdf4e5a5ff7c5ba1d643897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.chronicleWatchlist.ChronicleWatchlistEntityPopulationMechanism",
    jsii_struct_bases=[],
    name_mapping={"manual": "manual"},
)
class ChronicleWatchlistEntityPopulationMechanism:
    def __init__(
        self,
        *,
        manual: typing.Optional[typing.Union["ChronicleWatchlistEntityPopulationMechanismManual", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param manual: manual block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#manual ChronicleWatchlist#manual}
        '''
        if isinstance(manual, dict):
            manual = ChronicleWatchlistEntityPopulationMechanismManual(**manual)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b93573ddca3be56afa7acb36b565e5897545eddd847c97ed705ce239da09f6fd)
            check_type(argname="argument manual", value=manual, expected_type=type_hints["manual"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if manual is not None:
            self._values["manual"] = manual

    @builtins.property
    def manual(
        self,
    ) -> typing.Optional["ChronicleWatchlistEntityPopulationMechanismManual"]:
        '''manual block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#manual ChronicleWatchlist#manual}
        '''
        result = self._values.get("manual")
        return typing.cast(typing.Optional["ChronicleWatchlistEntityPopulationMechanismManual"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChronicleWatchlistEntityPopulationMechanism(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.chronicleWatchlist.ChronicleWatchlistEntityPopulationMechanismManual",
    jsii_struct_bases=[],
    name_mapping={},
)
class ChronicleWatchlistEntityPopulationMechanismManual:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChronicleWatchlistEntityPopulationMechanismManual(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChronicleWatchlistEntityPopulationMechanismManualOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleWatchlist.ChronicleWatchlistEntityPopulationMechanismManualOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffbeb6993cd9dd7c282ef1e202004f04e531f66a27c9c46836b5f26d02e73091)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChronicleWatchlistEntityPopulationMechanismManual]:
        return typing.cast(typing.Optional[ChronicleWatchlistEntityPopulationMechanismManual], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChronicleWatchlistEntityPopulationMechanismManual],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f25b62610f22143c4534090cc27da374873a943e589b756dc412f55c25d95a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ChronicleWatchlistEntityPopulationMechanismOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleWatchlist.ChronicleWatchlistEntityPopulationMechanismOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b96d14750b0b68f310a4185ec861ca80fd263480f5c6880fcc005815e3cd0fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putManual")
    def put_manual(self) -> None:
        value = ChronicleWatchlistEntityPopulationMechanismManual()

        return typing.cast(None, jsii.invoke(self, "putManual", [value]))

    @jsii.member(jsii_name="resetManual")
    def reset_manual(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManual", []))

    @builtins.property
    @jsii.member(jsii_name="manual")
    def manual(
        self,
    ) -> ChronicleWatchlistEntityPopulationMechanismManualOutputReference:
        return typing.cast(ChronicleWatchlistEntityPopulationMechanismManualOutputReference, jsii.get(self, "manual"))

    @builtins.property
    @jsii.member(jsii_name="manualInput")
    def manual_input(
        self,
    ) -> typing.Optional[ChronicleWatchlistEntityPopulationMechanismManual]:
        return typing.cast(typing.Optional[ChronicleWatchlistEntityPopulationMechanismManual], jsii.get(self, "manualInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChronicleWatchlistEntityPopulationMechanism]:
        return typing.cast(typing.Optional[ChronicleWatchlistEntityPopulationMechanism], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChronicleWatchlistEntityPopulationMechanism],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fc05626e13a3a169ca5997177753bafe4731cf58b11e2a3d00f3654cfa4b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.chronicleWatchlist.ChronicleWatchlistTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ChronicleWatchlistTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#create ChronicleWatchlist#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#delete ChronicleWatchlist#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#update ChronicleWatchlist#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a9509fdece471e01a302aeb1f75d47365d9188e0d4628665ea2c24cabebaba)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#create ChronicleWatchlist#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#delete ChronicleWatchlist#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#update ChronicleWatchlist#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChronicleWatchlistTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChronicleWatchlistTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleWatchlist.ChronicleWatchlistTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f80f03c6605f8f4b3422bd36e7addbb871aa3789921f129e3b56e730f79fea0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6d7a78cffa516a8a79c1b94d39d20aa86b90b2d574db3720b2d91afccafa439)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd344db86931d42508053f6989a2429dc25e4b7efee7de3b886f638a3403ac34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a45dd2700ee1b8930a578f9a7e62cf2c1226eb8aaf7608d174f6312e286fe9fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleWatchlistTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleWatchlistTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleWatchlistTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93bc40e77b2e59149080c0227253dea14ef23d36e1b504d4c70b7b6a3a9d8794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.chronicleWatchlist.ChronicleWatchlistWatchlistUserPreferences",
    jsii_struct_bases=[],
    name_mapping={"pinned": "pinned"},
)
class ChronicleWatchlistWatchlistUserPreferences:
    def __init__(
        self,
        *,
        pinned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pinned: Optional. Whether the watchlist is pinned on the dashboard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#pinned ChronicleWatchlist#pinned}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1369b13d3e93376dc9726b2bdf893dc55cc4ea4ca766c269076f901e3f4bac0)
            check_type(argname="argument pinned", value=pinned, expected_type=type_hints["pinned"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pinned is not None:
            self._values["pinned"] = pinned

    @builtins.property
    def pinned(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Whether the watchlist is pinned on the dashboard.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_watchlist#pinned ChronicleWatchlist#pinned}
        '''
        result = self._values.get("pinned")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChronicleWatchlistWatchlistUserPreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChronicleWatchlistWatchlistUserPreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleWatchlist.ChronicleWatchlistWatchlistUserPreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d691476a1240a236cb59bcfcf38cb4fe0ad0a77a80ecf624c814b178895e1277)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e451277ff44480e71aebf70ab633b59ca0275255a100602f4d9991f9a9d3b570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pinned", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChronicleWatchlistWatchlistUserPreferences]:
        return typing.cast(typing.Optional[ChronicleWatchlistWatchlistUserPreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChronicleWatchlistWatchlistUserPreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c76e63290d47d100b074a5f35ff70c48605fa4e5e3b8f745257a573644f3ed94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ChronicleWatchlist",
    "ChronicleWatchlistConfig",
    "ChronicleWatchlistEntityCount",
    "ChronicleWatchlistEntityCountList",
    "ChronicleWatchlistEntityCountOutputReference",
    "ChronicleWatchlistEntityPopulationMechanism",
    "ChronicleWatchlistEntityPopulationMechanismManual",
    "ChronicleWatchlistEntityPopulationMechanismManualOutputReference",
    "ChronicleWatchlistEntityPopulationMechanismOutputReference",
    "ChronicleWatchlistTimeouts",
    "ChronicleWatchlistTimeoutsOutputReference",
    "ChronicleWatchlistWatchlistUserPreferences",
    "ChronicleWatchlistWatchlistUserPreferencesOutputReference",
]

publication.publish()

def _typecheckingstub__9fd90a5bea53bd637b39d0b0ecbeb4424a14970cf9c38e96b10b5ca507d931aa(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    entity_population_mechanism: typing.Union[ChronicleWatchlistEntityPopulationMechanism, typing.Dict[builtins.str, typing.Any]],
    instance: builtins.str,
    location: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    multiplying_factor: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ChronicleWatchlistTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    watchlist_id: typing.Optional[builtins.str] = None,
    watchlist_user_preferences: typing.Optional[typing.Union[ChronicleWatchlistWatchlistUserPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0278d9c37c0b84008a6414fe4de471050e30c39f0ae304360984148fcbc307fd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3002ac90cadd9192f2a5aed40784cdc75d0934e2077ec05ae8c77dae2fa7fe59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5218b8cd574abe0d07139e4923c356def6f561a7483390055e8d20fa18c25214(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e2a6180c5ae63bac4168b3077e82af562a28d8732e2541539a24be29c9f5ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7916d00faaa1d00328366c363947beb9bc60ef876f4b29b54e8a722f00880c6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8505127ba0d798d56c432a09c732bf344951a48c46e00854729f52f3320e915b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e088f5dd99a618b70d0e0e706267946c5125935cc79f251f425036dba7ee8b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ef61f5c0355bbf14f136c383d859aa037160af21312b0c95cb716e00734191(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c610918e0b75e3347efeae7c74fb7d472cbbd5332dce157ca74d3508c03e0f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086d3265ae272408a8f928fe81ba72f73446ad2f9ed7159914defcbb5c285965(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    entity_population_mechanism: typing.Union[ChronicleWatchlistEntityPopulationMechanism, typing.Dict[builtins.str, typing.Any]],
    instance: builtins.str,
    location: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    multiplying_factor: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ChronicleWatchlistTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    watchlist_id: typing.Optional[builtins.str] = None,
    watchlist_user_preferences: typing.Optional[typing.Union[ChronicleWatchlistWatchlistUserPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5836a192d080a5cf4f9e37fe41cf792b74001cfc58c7e465093bbe4f667f87e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f1d6dfb03f9b350eb78966a64d855beeff2f5c05d72f621dfbea9b08c44e0d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6095540d9905b9fcf029977feec71987080f68ae16e1278caeb7bc531f4cdf5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3abc3065078d023d2b0f0a0c8334c13ec78ff17075ba1b8e512726f063bf6c99(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c30cfc2598cdc6f197dd4ad8ffa0b3adb064e45d2f27a0781849052fb90f643c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ab475238bbcd49c434abc6211757eb23be4de69b910c9c91f3e756237aa1e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c0c62358f168f532f86577ec4264467df7229a7ccdf4e5a5ff7c5ba1d643897(
    value: typing.Optional[ChronicleWatchlistEntityCount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93573ddca3be56afa7acb36b565e5897545eddd847c97ed705ce239da09f6fd(
    *,
    manual: typing.Optional[typing.Union[ChronicleWatchlistEntityPopulationMechanismManual, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffbeb6993cd9dd7c282ef1e202004f04e531f66a27c9c46836b5f26d02e73091(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f25b62610f22143c4534090cc27da374873a943e589b756dc412f55c25d95a(
    value: typing.Optional[ChronicleWatchlistEntityPopulationMechanismManual],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b96d14750b0b68f310a4185ec861ca80fd263480f5c6880fcc005815e3cd0fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fc05626e13a3a169ca5997177753bafe4731cf58b11e2a3d00f3654cfa4b09(
    value: typing.Optional[ChronicleWatchlistEntityPopulationMechanism],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a9509fdece471e01a302aeb1f75d47365d9188e0d4628665ea2c24cabebaba(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80f03c6605f8f4b3422bd36e7addbb871aa3789921f129e3b56e730f79fea0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d7a78cffa516a8a79c1b94d39d20aa86b90b2d574db3720b2d91afccafa439(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd344db86931d42508053f6989a2429dc25e4b7efee7de3b886f638a3403ac34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45dd2700ee1b8930a578f9a7e62cf2c1226eb8aaf7608d174f6312e286fe9fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93bc40e77b2e59149080c0227253dea14ef23d36e1b504d4c70b7b6a3a9d8794(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleWatchlistTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1369b13d3e93376dc9726b2bdf893dc55cc4ea4ca766c269076f901e3f4bac0(
    *,
    pinned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d691476a1240a236cb59bcfcf38cb4fe0ad0a77a80ecf624c814b178895e1277(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e451277ff44480e71aebf70ab633b59ca0275255a100602f4d9991f9a9d3b570(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76e63290d47d100b074a5f35ff70c48605fa4e5e3b8f745257a573644f3ed94(
    value: typing.Optional[ChronicleWatchlistWatchlistUserPreferences],
) -> None:
    """Type checking stubs"""
    pass
