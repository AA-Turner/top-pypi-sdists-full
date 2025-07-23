r'''
# `google_migration_center_preference_set`

Refer to the Terraform Registry for docs: [`google_migration_center_preference_set`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set).
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


class MigrationCenterPreferenceSet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSet",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set google_migration_center_preference_set}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        preference_set_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MigrationCenterPreferenceSetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine_preferences: typing.Optional[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set google_migration_center_preference_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Part of 'parent'. See documentation of 'projectsId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#location MigrationCenterPreferenceSet#location}
        :param preference_set_id: Required. User specified ID for the preference set. It will become the last component of the preference set name. The ID must be unique within the project, must conform with RFC-1034, is restricted to lower-cased letters, and has a maximum length of 63 characters. The ID must match the regular expression '`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#preference_set_id MigrationCenterPreferenceSet#preference_set_id}
        :param description: A description of the preference set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#description MigrationCenterPreferenceSet#description}
        :param display_name: User-friendly display name. Maximum length is 63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#display_name MigrationCenterPreferenceSet#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#id MigrationCenterPreferenceSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#project MigrationCenterPreferenceSet#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#timeouts MigrationCenterPreferenceSet#timeouts}
        :param virtual_machine_preferences: virtual_machine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#virtual_machine_preferences MigrationCenterPreferenceSet#virtual_machine_preferences}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f138716ca92b865846b5dcfbfddcc644218b8c1bb069ea8a9eaad6d1734ec5e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MigrationCenterPreferenceSetConfig(
            location=location,
            preference_set_id=preference_set_id,
            description=description,
            display_name=display_name,
            id=id,
            project=project,
            timeouts=timeouts,
            virtual_machine_preferences=virtual_machine_preferences,
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
        '''Generates CDKTF code for importing a MigrationCenterPreferenceSet resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MigrationCenterPreferenceSet to import.
        :param import_from_id: The id of the existing MigrationCenterPreferenceSet that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MigrationCenterPreferenceSet to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b6a621ecf5b1ec3fefc1cd9c08233a5b1ba8afe944e9e4c8521876f8fd2509)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#create MigrationCenterPreferenceSet#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#delete MigrationCenterPreferenceSet#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#update MigrationCenterPreferenceSet#update}.
        '''
        value = MigrationCenterPreferenceSetTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualMachinePreferences")
    def put_virtual_machine_preferences(
        self,
        *,
        commitment_plan: typing.Optional[builtins.str] = None,
        compute_engine_preferences: typing.Optional[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        region_preferences: typing.Optional[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        sizing_optimization_strategy: typing.Optional[builtins.str] = None,
        sole_tenancy_preferences: typing.Optional[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        target_product: typing.Optional[builtins.str] = None,
        vmware_engine_preferences: typing.Optional[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param commitment_plan: Commitment plan to consider when calculating costs for virtual machine insights and recommendations. If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'COMMITMENT_PLAN_NONE', 'COMMITMENT_PLAN_ONE_YEAR', 'COMMITMENT_PLAN_THREE_YEARS' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#commitment_plan MigrationCenterPreferenceSet#commitment_plan}
        :param compute_engine_preferences: compute_engine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#compute_engine_preferences MigrationCenterPreferenceSet#compute_engine_preferences}
        :param region_preferences: region_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#region_preferences MigrationCenterPreferenceSet#region_preferences}
        :param sizing_optimization_strategy: Sizing optimization strategy specifies the preferred strategy used when extrapolating usage data to calculate insights and recommendations for a virtual machine. If you are unsure which value to set, a moderate sizing optimization strategy is often a good value to start with. Possible values: 'SIZING_OPTIMIZATION_STRATEGY_UNSPECIFIED', 'SIZING_OPTIMIZATION_STRATEGY_SAME_AS_SOURCE', 'SIZING_OPTIMIZATION_STRATEGY_MODERATE', 'SIZING_OPTIMIZATION_STRATEGY_AGGRESSIVE' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#sizing_optimization_strategy MigrationCenterPreferenceSet#sizing_optimization_strategy}
        :param sole_tenancy_preferences: sole_tenancy_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#sole_tenancy_preferences MigrationCenterPreferenceSet#sole_tenancy_preferences}
        :param target_product: Target product for assets using this preference set. Specify either target product or business goal, but not both. Possible values: 'COMPUTE_MIGRATION_TARGET_PRODUCT_UNSPECIFIED', 'COMPUTE_MIGRATION_TARGET_PRODUCT_COMPUTE_ENGINE', 'COMPUTE_MIGRATION_TARGET_PRODUCT_VMWARE_ENGINE', 'COMPUTE_MIGRATION_TARGET_PRODUCT_SOLE_TENANCY' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#target_product MigrationCenterPreferenceSet#target_product}
        :param vmware_engine_preferences: vmware_engine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#vmware_engine_preferences MigrationCenterPreferenceSet#vmware_engine_preferences}
        '''
        value = MigrationCenterPreferenceSetVirtualMachinePreferences(
            commitment_plan=commitment_plan,
            compute_engine_preferences=compute_engine_preferences,
            region_preferences=region_preferences,
            sizing_optimization_strategy=sizing_optimization_strategy,
            sole_tenancy_preferences=sole_tenancy_preferences,
            target_product=target_product,
            vmware_engine_preferences=vmware_engine_preferences,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualMachinePreferences", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualMachinePreferences")
    def reset_virtual_machine_preferences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachinePreferences", []))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MigrationCenterPreferenceSetTimeoutsOutputReference":
        return typing.cast("MigrationCenterPreferenceSetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachinePreferences")
    def virtual_machine_preferences(
        self,
    ) -> "MigrationCenterPreferenceSetVirtualMachinePreferencesOutputReference":
        return typing.cast("MigrationCenterPreferenceSetVirtualMachinePreferencesOutputReference", jsii.get(self, "virtualMachinePreferences"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="preferenceSetIdInput")
    def preference_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferenceSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MigrationCenterPreferenceSetTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MigrationCenterPreferenceSetTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachinePreferencesInput")
    def virtual_machine_preferences_input(
        self,
    ) -> typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferences"]:
        return typing.cast(typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferences"], jsii.get(self, "virtualMachinePreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a22af2ca2f609eb6e295fbb98a1410237a7ab4f86a4c70bed2d276c9851d4d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f632ac1e538ed1e8efc014fcebfb1b8d6ea9306a060dd566d418b611c0ebad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281aff1a7c1797a7cf0fdf582cbea7fa7cc7f978b590e9fe75fbc625c674f0c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f0e23f023d19fbb7cf0d8807e63c9858d869f7fb648e16d195d43f966f3782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferenceSetId")
    def preference_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferenceSetId"))

    @preference_set_id.setter
    def preference_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f7d13bab51c1fd1f38a10bb963d5d46a3e3240344c8fd030075de0d26e94f23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferenceSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d09ee579fbf55cf25e6f75b11f329285ac89b3ba00cb68dacc0ba0e1ac31d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "preference_set_id": "preferenceSetId",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
        "virtual_machine_preferences": "virtualMachinePreferences",
    },
)
class MigrationCenterPreferenceSetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        preference_set_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MigrationCenterPreferenceSetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine_preferences: typing.Optional[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Part of 'parent'. See documentation of 'projectsId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#location MigrationCenterPreferenceSet#location}
        :param preference_set_id: Required. User specified ID for the preference set. It will become the last component of the preference set name. The ID must be unique within the project, must conform with RFC-1034, is restricted to lower-cased letters, and has a maximum length of 63 characters. The ID must match the regular expression '`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#preference_set_id MigrationCenterPreferenceSet#preference_set_id}
        :param description: A description of the preference set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#description MigrationCenterPreferenceSet#description}
        :param display_name: User-friendly display name. Maximum length is 63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#display_name MigrationCenterPreferenceSet#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#id MigrationCenterPreferenceSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#project MigrationCenterPreferenceSet#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#timeouts MigrationCenterPreferenceSet#timeouts}
        :param virtual_machine_preferences: virtual_machine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#virtual_machine_preferences MigrationCenterPreferenceSet#virtual_machine_preferences}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = MigrationCenterPreferenceSetTimeouts(**timeouts)
        if isinstance(virtual_machine_preferences, dict):
            virtual_machine_preferences = MigrationCenterPreferenceSetVirtualMachinePreferences(**virtual_machine_preferences)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29bc577b313c7cb0292c66faa10d641d6955000546fd0b26bddf60c6bb7a5ec)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument preference_set_id", value=preference_set_id, expected_type=type_hints["preference_set_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_machine_preferences", value=virtual_machine_preferences, expected_type=type_hints["virtual_machine_preferences"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "preference_set_id": preference_set_id,
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
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_machine_preferences is not None:
            self._values["virtual_machine_preferences"] = virtual_machine_preferences

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
    def location(self) -> builtins.str:
        '''Part of 'parent'. See documentation of 'projectsId'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#location MigrationCenterPreferenceSet#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def preference_set_id(self) -> builtins.str:
        '''Required.

        User specified ID for the preference set. It will become the last component of the preference set name. The ID must be unique within the project, must conform with RFC-1034, is restricted to lower-cased letters, and has a maximum length of 63 characters. The ID must match the regular expression '`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#preference_set_id MigrationCenterPreferenceSet#preference_set_id}
        '''
        result = self._values.get("preference_set_id")
        assert result is not None, "Required property 'preference_set_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the preference set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#description MigrationCenterPreferenceSet#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User-friendly display name. Maximum length is 63 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#display_name MigrationCenterPreferenceSet#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#id MigrationCenterPreferenceSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#project MigrationCenterPreferenceSet#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MigrationCenterPreferenceSetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#timeouts MigrationCenterPreferenceSet#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MigrationCenterPreferenceSetTimeouts"], result)

    @builtins.property
    def virtual_machine_preferences(
        self,
    ) -> typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferences"]:
        '''virtual_machine_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#virtual_machine_preferences MigrationCenterPreferenceSet#virtual_machine_preferences}
        '''
        result = self._values.get("virtual_machine_preferences")
        return typing.cast(typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferences"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MigrationCenterPreferenceSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class MigrationCenterPreferenceSetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#create MigrationCenterPreferenceSet#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#delete MigrationCenterPreferenceSet#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#update MigrationCenterPreferenceSet#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776449334e17d7e5a6b0689bffdef9e9b3ecc7a46b63a861da220273f8a5ed9f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#create MigrationCenterPreferenceSet#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#delete MigrationCenterPreferenceSet#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#update MigrationCenterPreferenceSet#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MigrationCenterPreferenceSetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MigrationCenterPreferenceSetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb38dbfb276ba51d6ac74e5856f87e1d6000e22342be720fc0b21ff70853c0f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8494478e9e659c6915067262f7cde9399cb150d591951736f3501e376b81fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fb08773caa959ba1507cb54590312069171ba593259a12201453df68c12cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1789e70f4dcc102669202e009abacf47edbfd0332a3550269250c1ce9a75b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MigrationCenterPreferenceSetTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MigrationCenterPreferenceSetTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MigrationCenterPreferenceSetTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2dfd384c10bef3bcd6e42a78f2beb95d2d59db21661b48a3f91bb2cfc1e70cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferences",
    jsii_struct_bases=[],
    name_mapping={
        "commitment_plan": "commitmentPlan",
        "compute_engine_preferences": "computeEnginePreferences",
        "region_preferences": "regionPreferences",
        "sizing_optimization_strategy": "sizingOptimizationStrategy",
        "sole_tenancy_preferences": "soleTenancyPreferences",
        "target_product": "targetProduct",
        "vmware_engine_preferences": "vmwareEnginePreferences",
    },
)
class MigrationCenterPreferenceSetVirtualMachinePreferences:
    def __init__(
        self,
        *,
        commitment_plan: typing.Optional[builtins.str] = None,
        compute_engine_preferences: typing.Optional[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        region_preferences: typing.Optional[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        sizing_optimization_strategy: typing.Optional[builtins.str] = None,
        sole_tenancy_preferences: typing.Optional[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        target_product: typing.Optional[builtins.str] = None,
        vmware_engine_preferences: typing.Optional[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param commitment_plan: Commitment plan to consider when calculating costs for virtual machine insights and recommendations. If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'COMMITMENT_PLAN_NONE', 'COMMITMENT_PLAN_ONE_YEAR', 'COMMITMENT_PLAN_THREE_YEARS' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#commitment_plan MigrationCenterPreferenceSet#commitment_plan}
        :param compute_engine_preferences: compute_engine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#compute_engine_preferences MigrationCenterPreferenceSet#compute_engine_preferences}
        :param region_preferences: region_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#region_preferences MigrationCenterPreferenceSet#region_preferences}
        :param sizing_optimization_strategy: Sizing optimization strategy specifies the preferred strategy used when extrapolating usage data to calculate insights and recommendations for a virtual machine. If you are unsure which value to set, a moderate sizing optimization strategy is often a good value to start with. Possible values: 'SIZING_OPTIMIZATION_STRATEGY_UNSPECIFIED', 'SIZING_OPTIMIZATION_STRATEGY_SAME_AS_SOURCE', 'SIZING_OPTIMIZATION_STRATEGY_MODERATE', 'SIZING_OPTIMIZATION_STRATEGY_AGGRESSIVE' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#sizing_optimization_strategy MigrationCenterPreferenceSet#sizing_optimization_strategy}
        :param sole_tenancy_preferences: sole_tenancy_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#sole_tenancy_preferences MigrationCenterPreferenceSet#sole_tenancy_preferences}
        :param target_product: Target product for assets using this preference set. Specify either target product or business goal, but not both. Possible values: 'COMPUTE_MIGRATION_TARGET_PRODUCT_UNSPECIFIED', 'COMPUTE_MIGRATION_TARGET_PRODUCT_COMPUTE_ENGINE', 'COMPUTE_MIGRATION_TARGET_PRODUCT_VMWARE_ENGINE', 'COMPUTE_MIGRATION_TARGET_PRODUCT_SOLE_TENANCY' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#target_product MigrationCenterPreferenceSet#target_product}
        :param vmware_engine_preferences: vmware_engine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#vmware_engine_preferences MigrationCenterPreferenceSet#vmware_engine_preferences}
        '''
        if isinstance(compute_engine_preferences, dict):
            compute_engine_preferences = MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences(**compute_engine_preferences)
        if isinstance(region_preferences, dict):
            region_preferences = MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences(**region_preferences)
        if isinstance(sole_tenancy_preferences, dict):
            sole_tenancy_preferences = MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences(**sole_tenancy_preferences)
        if isinstance(vmware_engine_preferences, dict):
            vmware_engine_preferences = MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences(**vmware_engine_preferences)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5316eb4a0e659e46ff47e27e2e03f89c51c18363812cac045ab1cfd5b07aa5d)
            check_type(argname="argument commitment_plan", value=commitment_plan, expected_type=type_hints["commitment_plan"])
            check_type(argname="argument compute_engine_preferences", value=compute_engine_preferences, expected_type=type_hints["compute_engine_preferences"])
            check_type(argname="argument region_preferences", value=region_preferences, expected_type=type_hints["region_preferences"])
            check_type(argname="argument sizing_optimization_strategy", value=sizing_optimization_strategy, expected_type=type_hints["sizing_optimization_strategy"])
            check_type(argname="argument sole_tenancy_preferences", value=sole_tenancy_preferences, expected_type=type_hints["sole_tenancy_preferences"])
            check_type(argname="argument target_product", value=target_product, expected_type=type_hints["target_product"])
            check_type(argname="argument vmware_engine_preferences", value=vmware_engine_preferences, expected_type=type_hints["vmware_engine_preferences"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if commitment_plan is not None:
            self._values["commitment_plan"] = commitment_plan
        if compute_engine_preferences is not None:
            self._values["compute_engine_preferences"] = compute_engine_preferences
        if region_preferences is not None:
            self._values["region_preferences"] = region_preferences
        if sizing_optimization_strategy is not None:
            self._values["sizing_optimization_strategy"] = sizing_optimization_strategy
        if sole_tenancy_preferences is not None:
            self._values["sole_tenancy_preferences"] = sole_tenancy_preferences
        if target_product is not None:
            self._values["target_product"] = target_product
        if vmware_engine_preferences is not None:
            self._values["vmware_engine_preferences"] = vmware_engine_preferences

    @builtins.property
    def commitment_plan(self) -> typing.Optional[builtins.str]:
        '''Commitment plan to consider when calculating costs for virtual machine insights and recommendations.

        If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'COMMITMENT_PLAN_NONE', 'COMMITMENT_PLAN_ONE_YEAR', 'COMMITMENT_PLAN_THREE_YEARS'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#commitment_plan MigrationCenterPreferenceSet#commitment_plan}
        '''
        result = self._values.get("commitment_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_engine_preferences(
        self,
    ) -> typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences"]:
        '''compute_engine_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#compute_engine_preferences MigrationCenterPreferenceSet#compute_engine_preferences}
        '''
        result = self._values.get("compute_engine_preferences")
        return typing.cast(typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences"], result)

    @builtins.property
    def region_preferences(
        self,
    ) -> typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences"]:
        '''region_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#region_preferences MigrationCenterPreferenceSet#region_preferences}
        '''
        result = self._values.get("region_preferences")
        return typing.cast(typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences"], result)

    @builtins.property
    def sizing_optimization_strategy(self) -> typing.Optional[builtins.str]:
        '''Sizing optimization strategy specifies the preferred strategy used when extrapolating usage data to calculate insights and recommendations for a virtual machine.

        If you are unsure which value to set, a moderate sizing optimization strategy is often a good value to start with. Possible values: 'SIZING_OPTIMIZATION_STRATEGY_UNSPECIFIED', 'SIZING_OPTIMIZATION_STRATEGY_SAME_AS_SOURCE', 'SIZING_OPTIMIZATION_STRATEGY_MODERATE', 'SIZING_OPTIMIZATION_STRATEGY_AGGRESSIVE'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#sizing_optimization_strategy MigrationCenterPreferenceSet#sizing_optimization_strategy}
        '''
        result = self._values.get("sizing_optimization_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sole_tenancy_preferences(
        self,
    ) -> typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences"]:
        '''sole_tenancy_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#sole_tenancy_preferences MigrationCenterPreferenceSet#sole_tenancy_preferences}
        '''
        result = self._values.get("sole_tenancy_preferences")
        return typing.cast(typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences"], result)

    @builtins.property
    def target_product(self) -> typing.Optional[builtins.str]:
        '''Target product for assets using this preference set.

        Specify either target product or business goal, but not both. Possible values: 'COMPUTE_MIGRATION_TARGET_PRODUCT_UNSPECIFIED', 'COMPUTE_MIGRATION_TARGET_PRODUCT_COMPUTE_ENGINE', 'COMPUTE_MIGRATION_TARGET_PRODUCT_VMWARE_ENGINE', 'COMPUTE_MIGRATION_TARGET_PRODUCT_SOLE_TENANCY'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#target_product MigrationCenterPreferenceSet#target_product}
        '''
        result = self._values.get("target_product")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vmware_engine_preferences(
        self,
    ) -> typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences"]:
        '''vmware_engine_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#vmware_engine_preferences MigrationCenterPreferenceSet#vmware_engine_preferences}
        '''
        result = self._values.get("vmware_engine_preferences")
        return typing.cast(typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MigrationCenterPreferenceSetVirtualMachinePreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences",
    jsii_struct_bases=[],
    name_mapping={
        "license_type": "licenseType",
        "machine_preferences": "machinePreferences",
    },
)
class MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences:
    def __init__(
        self,
        *,
        license_type: typing.Optional[builtins.str] = None,
        machine_preferences: typing.Optional[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param license_type: License type to consider when calculating costs for virtual machine insights and recommendations. If unspecified, costs are calculated based on the default licensing plan. Possible values: 'LICENSE_TYPE_UNSPECIFIED', 'LICENSE_TYPE_DEFAULT', 'LICENSE_TYPE_BRING_YOUR_OWN_LICENSE' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#license_type MigrationCenterPreferenceSet#license_type}
        :param machine_preferences: machine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#machine_preferences MigrationCenterPreferenceSet#machine_preferences}
        '''
        if isinstance(machine_preferences, dict):
            machine_preferences = MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences(**machine_preferences)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed37e68e07fd090d97e0c3bd9d0574827af665772360aca55160fb104e324d1)
            check_type(argname="argument license_type", value=license_type, expected_type=type_hints["license_type"])
            check_type(argname="argument machine_preferences", value=machine_preferences, expected_type=type_hints["machine_preferences"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if license_type is not None:
            self._values["license_type"] = license_type
        if machine_preferences is not None:
            self._values["machine_preferences"] = machine_preferences

    @builtins.property
    def license_type(self) -> typing.Optional[builtins.str]:
        '''License type to consider when calculating costs for virtual machine insights and recommendations.

        If unspecified, costs are calculated based on the default licensing plan. Possible values: 'LICENSE_TYPE_UNSPECIFIED', 'LICENSE_TYPE_DEFAULT', 'LICENSE_TYPE_BRING_YOUR_OWN_LICENSE'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#license_type MigrationCenterPreferenceSet#license_type}
        '''
        result = self._values.get("license_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_preferences(
        self,
    ) -> typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences"]:
        '''machine_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#machine_preferences MigrationCenterPreferenceSet#machine_preferences}
        '''
        result = self._values.get("machine_preferences")
        return typing.cast(typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences",
    jsii_struct_bases=[],
    name_mapping={"allowed_machine_series": "allowedMachineSeries"},
)
class MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences:
    def __init__(
        self,
        *,
        allowed_machine_series: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_machine_series: allowed_machine_series block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#allowed_machine_series MigrationCenterPreferenceSet#allowed_machine_series}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76bd1b748eb66ab025c82b10d352ac1eb4ca9d0df41d8fbc0236670839f6cf0)
            check_type(argname="argument allowed_machine_series", value=allowed_machine_series, expected_type=type_hints["allowed_machine_series"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_machine_series is not None:
            self._values["allowed_machine_series"] = allowed_machine_series

    @builtins.property
    def allowed_machine_series(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries"]]]:
        '''allowed_machine_series block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#allowed_machine_series MigrationCenterPreferenceSet#allowed_machine_series}
        '''
        result = self._values.get("allowed_machine_series")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries",
    jsii_struct_bases=[],
    name_mapping={"code": "code"},
)
class MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries:
    def __init__(self, *, code: typing.Optional[builtins.str] = None) -> None:
        '''
        :param code: Code to identify a Compute Engine machine series. Consult https://cloud.google.com/compute/docs/machine-resource#machine_type_comparison for more details on the available series. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#code MigrationCenterPreferenceSet#code}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed562e28bdbeb2b51f0fcd060a037c19f8d4fa751786dee72d20f14b994382cc)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code is not None:
            self._values["code"] = code

    @builtins.property
    def code(self) -> typing.Optional[builtins.str]:
        '''Code to identify a Compute Engine machine series. Consult https://cloud.google.com/compute/docs/machine-resource#machine_type_comparison for more details on the available series.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#code MigrationCenterPreferenceSet#code}
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a2e50095f85abf7187f22c532b5d1d6c7e61e504d86d77b95459b04a5e43da0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b943025d283f3018d7db8f78659f32d62cd70e45d2bb2f295d41d8a3fb9fbc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35eecf8c5e82b52120b4e82b5338b473a99815cbcb5da28ce585675d1b5ed4dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e2219d395558a5e1ebf8b41496c2e9ccdfdedb15295569eab485bae7db6e7e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__251eb033e252ae1ef3c7d2a88357fa78c83e94c2b8699643259721de541c6d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e2c615c272616ca4adc326dd65716e2b3a5687b2096df3d4ac46eb0b6209a1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8777157a16cce46977546a191c553f439408fc4b5f838218be4914dbe29dac2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCode")
    def reset_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCode", []))

    @builtins.property
    @jsii.member(jsii_name="codeInput")
    def code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeInput"))

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "code"))

    @code.setter
    def code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d453855a85325ca63dcc11241deabfbf74a1573dacf67936c417b195a895fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02fbb0382301ceba9a8db12e02ce6459d2945ca49a51ec9de22797468531027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a943ec54e985294e0331c10980b6ee68d216857c72ecbc3c0da003795c08236e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllowedMachineSeries")
    def put_allowed_machine_series(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f0c3649fc6028d7feec078c062cbd1e61bbbe42e1f15fa0632d660108502cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedMachineSeries", [value]))

    @jsii.member(jsii_name="resetAllowedMachineSeries")
    def reset_allowed_machine_series(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedMachineSeries", []))

    @builtins.property
    @jsii.member(jsii_name="allowedMachineSeries")
    def allowed_machine_series(
        self,
    ) -> MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesList:
        return typing.cast(MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesList, jsii.get(self, "allowedMachineSeries"))

    @builtins.property
    @jsii.member(jsii_name="allowedMachineSeriesInput")
    def allowed_machine_series_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]], jsii.get(self, "allowedMachineSeriesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences]:
        return typing.cast(typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5fc3080f684c9274045496f91e062cd7e4feea4f6985fdd650befecc90acf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d36c88806c42ffeccb6b331b81e837834f582a467e46012b8e35bdaedb41463f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMachinePreferences")
    def put_machine_preferences(
        self,
        *,
        allowed_machine_series: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_machine_series: allowed_machine_series block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#allowed_machine_series MigrationCenterPreferenceSet#allowed_machine_series}
        '''
        value = MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences(
            allowed_machine_series=allowed_machine_series
        )

        return typing.cast(None, jsii.invoke(self, "putMachinePreferences", [value]))

    @jsii.member(jsii_name="resetLicenseType")
    def reset_license_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenseType", []))

    @jsii.member(jsii_name="resetMachinePreferences")
    def reset_machine_preferences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachinePreferences", []))

    @builtins.property
    @jsii.member(jsii_name="machinePreferences")
    def machine_preferences(
        self,
    ) -> MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesOutputReference:
        return typing.cast(MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesOutputReference, jsii.get(self, "machinePreferences"))

    @builtins.property
    @jsii.member(jsii_name="licenseTypeInput")
    def license_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="machinePreferencesInput")
    def machine_preferences_input(
        self,
    ) -> typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences]:
        return typing.cast(typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences], jsii.get(self, "machinePreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseType")
    def license_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseType"))

    @license_type.setter
    def license_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ac28976997d454341c4012497d6565566085ff2fdbdc17cc39d9d11fb4abb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences]:
        return typing.cast(typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f1b09805e69cefc2d22a1171df8850812ae79a7fa52d200c417f1d2190ef40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MigrationCenterPreferenceSetVirtualMachinePreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e9ad3552fd4426060b07f162faedfa5dbbda3a4c03fe4e5e335afcd480516b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putComputeEnginePreferences")
    def put_compute_engine_preferences(
        self,
        *,
        license_type: typing.Optional[builtins.str] = None,
        machine_preferences: typing.Optional[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param license_type: License type to consider when calculating costs for virtual machine insights and recommendations. If unspecified, costs are calculated based on the default licensing plan. Possible values: 'LICENSE_TYPE_UNSPECIFIED', 'LICENSE_TYPE_DEFAULT', 'LICENSE_TYPE_BRING_YOUR_OWN_LICENSE' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#license_type MigrationCenterPreferenceSet#license_type}
        :param machine_preferences: machine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#machine_preferences MigrationCenterPreferenceSet#machine_preferences}
        '''
        value = MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences(
            license_type=license_type, machine_preferences=machine_preferences
        )

        return typing.cast(None, jsii.invoke(self, "putComputeEnginePreferences", [value]))

    @jsii.member(jsii_name="putRegionPreferences")
    def put_region_preferences(
        self,
        *,
        preferred_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param preferred_regions: A list of preferred regions, ordered by the most preferred region first. Set only valid Google Cloud region names. See https://cloud.google.com/compute/docs/regions-zones for available regions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#preferred_regions MigrationCenterPreferenceSet#preferred_regions}
        '''
        value = MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences(
            preferred_regions=preferred_regions
        )

        return typing.cast(None, jsii.invoke(self, "putRegionPreferences", [value]))

    @jsii.member(jsii_name="putSoleTenancyPreferences")
    def put_sole_tenancy_preferences(
        self,
        *,
        commitment_plan: typing.Optional[builtins.str] = None,
        cpu_overcommit_ratio: typing.Optional[jsii.Number] = None,
        host_maintenance_policy: typing.Optional[builtins.str] = None,
        node_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param commitment_plan: Commitment plan to consider when calculating costs for virtual machine insights and recommendations. If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'ON_DEMAND', 'COMMITMENT_1_YEAR', 'COMMITMENT_3_YEAR' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#commitment_plan MigrationCenterPreferenceSet#commitment_plan}
        :param cpu_overcommit_ratio: CPU overcommit ratio. Acceptable values are between 1.0 and 2.0 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#cpu_overcommit_ratio MigrationCenterPreferenceSet#cpu_overcommit_ratio}
        :param host_maintenance_policy: Sole Tenancy nodes maintenance policy. Possible values: 'HOST_MAINTENANCE_POLICY_UNSPECIFIED', 'HOST_MAINTENANCE_POLICY_DEFAULT', 'HOST_MAINTENANCE_POLICY_RESTART_IN_PLACE', 'HOST_MAINTENANCE_POLICY_MIGRATE_WITHIN_NODE_GROUP'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#host_maintenance_policy MigrationCenterPreferenceSet#host_maintenance_policy}
        :param node_types: node_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#node_types MigrationCenterPreferenceSet#node_types}
        '''
        value = MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences(
            commitment_plan=commitment_plan,
            cpu_overcommit_ratio=cpu_overcommit_ratio,
            host_maintenance_policy=host_maintenance_policy,
            node_types=node_types,
        )

        return typing.cast(None, jsii.invoke(self, "putSoleTenancyPreferences", [value]))

    @jsii.member(jsii_name="putVmwareEnginePreferences")
    def put_vmware_engine_preferences(
        self,
        *,
        commitment_plan: typing.Optional[builtins.str] = None,
        cpu_overcommit_ratio: typing.Optional[jsii.Number] = None,
        memory_overcommit_ratio: typing.Optional[jsii.Number] = None,
        storage_deduplication_compression_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param commitment_plan: Commitment plan to consider when calculating costs for virtual machine insights and recommendations. If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'ON_DEMAND', 'COMMITMENT_1_YEAR_MONTHLY_PAYMENTS', 'COMMITMENT_3_YEAR_MONTHLY_PAYMENTS', 'COMMITMENT_1_YEAR_UPFRONT_PAYMENT', 'COMMITMENT_3_YEAR_UPFRONT_PAYMENT', Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#commitment_plan MigrationCenterPreferenceSet#commitment_plan}
        :param cpu_overcommit_ratio: CPU overcommit ratio. Acceptable values are between 1.0 and 8.0, with 0.1 increment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#cpu_overcommit_ratio MigrationCenterPreferenceSet#cpu_overcommit_ratio}
        :param memory_overcommit_ratio: Memory overcommit ratio. Acceptable values are 1.0, 1.25, 1.5, 1.75 and 2.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#memory_overcommit_ratio MigrationCenterPreferenceSet#memory_overcommit_ratio}
        :param storage_deduplication_compression_ratio: The Deduplication and Compression ratio is based on the logical (Used Before) space required to store data before applying deduplication and compression, in relation to the physical (Used After) space required after applying deduplication and compression. Specifically, the ratio is the Used Before space divided by the Used After space. For example, if the Used Before space is 3 GB, but the physical Used After space is 1 GB, the deduplication and compression ratio is 3x. Acceptable values are between 1.0 and 4.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#storage_deduplication_compression_ratio MigrationCenterPreferenceSet#storage_deduplication_compression_ratio}
        '''
        value = MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences(
            commitment_plan=commitment_plan,
            cpu_overcommit_ratio=cpu_overcommit_ratio,
            memory_overcommit_ratio=memory_overcommit_ratio,
            storage_deduplication_compression_ratio=storage_deduplication_compression_ratio,
        )

        return typing.cast(None, jsii.invoke(self, "putVmwareEnginePreferences", [value]))

    @jsii.member(jsii_name="resetCommitmentPlan")
    def reset_commitment_plan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitmentPlan", []))

    @jsii.member(jsii_name="resetComputeEnginePreferences")
    def reset_compute_engine_preferences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeEnginePreferences", []))

    @jsii.member(jsii_name="resetRegionPreferences")
    def reset_region_preferences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionPreferences", []))

    @jsii.member(jsii_name="resetSizingOptimizationStrategy")
    def reset_sizing_optimization_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizingOptimizationStrategy", []))

    @jsii.member(jsii_name="resetSoleTenancyPreferences")
    def reset_sole_tenancy_preferences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSoleTenancyPreferences", []))

    @jsii.member(jsii_name="resetTargetProduct")
    def reset_target_product(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetProduct", []))

    @jsii.member(jsii_name="resetVmwareEnginePreferences")
    def reset_vmware_engine_preferences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmwareEnginePreferences", []))

    @builtins.property
    @jsii.member(jsii_name="computeEnginePreferences")
    def compute_engine_preferences(
        self,
    ) -> MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesOutputReference:
        return typing.cast(MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesOutputReference, jsii.get(self, "computeEnginePreferences"))

    @builtins.property
    @jsii.member(jsii_name="regionPreferences")
    def region_preferences(
        self,
    ) -> "MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferencesOutputReference":
        return typing.cast("MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferencesOutputReference", jsii.get(self, "regionPreferences"))

    @builtins.property
    @jsii.member(jsii_name="soleTenancyPreferences")
    def sole_tenancy_preferences(
        self,
    ) -> "MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesOutputReference":
        return typing.cast("MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesOutputReference", jsii.get(self, "soleTenancyPreferences"))

    @builtins.property
    @jsii.member(jsii_name="vmwareEnginePreferences")
    def vmware_engine_preferences(
        self,
    ) -> "MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferencesOutputReference":
        return typing.cast("MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferencesOutputReference", jsii.get(self, "vmwareEnginePreferences"))

    @builtins.property
    @jsii.member(jsii_name="commitmentPlanInput")
    def commitment_plan_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitmentPlanInput"))

    @builtins.property
    @jsii.member(jsii_name="computeEnginePreferencesInput")
    def compute_engine_preferences_input(
        self,
    ) -> typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences]:
        return typing.cast(typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences], jsii.get(self, "computeEnginePreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="regionPreferencesInput")
    def region_preferences_input(
        self,
    ) -> typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences"]:
        return typing.cast(typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences"], jsii.get(self, "regionPreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="sizingOptimizationStrategyInput")
    def sizing_optimization_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizingOptimizationStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="soleTenancyPreferencesInput")
    def sole_tenancy_preferences_input(
        self,
    ) -> typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences"]:
        return typing.cast(typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences"], jsii.get(self, "soleTenancyPreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetProductInput")
    def target_product_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetProductInput"))

    @builtins.property
    @jsii.member(jsii_name="vmwareEnginePreferencesInput")
    def vmware_engine_preferences_input(
        self,
    ) -> typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences"]:
        return typing.cast(typing.Optional["MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences"], jsii.get(self, "vmwareEnginePreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="commitmentPlan")
    def commitment_plan(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitmentPlan"))

    @commitment_plan.setter
    def commitment_plan(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d613230f60f3b10b3b74fab8e59b82169321de1eddd3310c7bae1c66767fe2fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitmentPlan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizingOptimizationStrategy")
    def sizing_optimization_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizingOptimizationStrategy"))

    @sizing_optimization_strategy.setter
    def sizing_optimization_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630f5c0f505639026b719b91725b9b89e5c012a4da313b5be3aaa1cb64fe2bd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizingOptimizationStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetProduct")
    def target_product(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetProduct"))

    @target_product.setter
    def target_product(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b44ca312918d6f0dfdd0fbce9b657a52b59080d91f69405236e09a99f9bac85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetProduct", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferences]:
        return typing.cast(typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d19f9c27a62882264100c6f38548e63fa62ed0ca4d23a36988da1abd95e69f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences",
    jsii_struct_bases=[],
    name_mapping={"preferred_regions": "preferredRegions"},
)
class MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences:
    def __init__(
        self,
        *,
        preferred_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param preferred_regions: A list of preferred regions, ordered by the most preferred region first. Set only valid Google Cloud region names. See https://cloud.google.com/compute/docs/regions-zones for available regions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#preferred_regions MigrationCenterPreferenceSet#preferred_regions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e88c3612465744f8106a2a85f58151c28ebb5e6085f5b0f1053a32fd3fc562bc)
            check_type(argname="argument preferred_regions", value=preferred_regions, expected_type=type_hints["preferred_regions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if preferred_regions is not None:
            self._values["preferred_regions"] = preferred_regions

    @builtins.property
    def preferred_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of preferred regions, ordered by the most preferred region first.

        Set only valid Google Cloud region names. See https://cloud.google.com/compute/docs/regions-zones for available regions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#preferred_regions MigrationCenterPreferenceSet#preferred_regions}
        '''
        result = self._values.get("preferred_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a03267703ce3a5a3e6e31a50f49be4b2e5b1fe6095b28064350c81f95a3fe1b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPreferredRegions")
    def reset_preferred_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredRegions", []))

    @builtins.property
    @jsii.member(jsii_name="preferredRegionsInput")
    def preferred_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "preferredRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredRegions")
    def preferred_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "preferredRegions"))

    @preferred_regions.setter
    def preferred_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995282a7df4e61b30e96fb4642b05c75a1a4165c63d61ba8de18a17d7a43d255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences]:
        return typing.cast(typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ee77c5f62e1500b1a94124c08a5bdadc70ce79ec001e9358bf3c32656448c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences",
    jsii_struct_bases=[],
    name_mapping={
        "commitment_plan": "commitmentPlan",
        "cpu_overcommit_ratio": "cpuOvercommitRatio",
        "host_maintenance_policy": "hostMaintenancePolicy",
        "node_types": "nodeTypes",
    },
)
class MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences:
    def __init__(
        self,
        *,
        commitment_plan: typing.Optional[builtins.str] = None,
        cpu_overcommit_ratio: typing.Optional[jsii.Number] = None,
        host_maintenance_policy: typing.Optional[builtins.str] = None,
        node_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param commitment_plan: Commitment plan to consider when calculating costs for virtual machine insights and recommendations. If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'ON_DEMAND', 'COMMITMENT_1_YEAR', 'COMMITMENT_3_YEAR' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#commitment_plan MigrationCenterPreferenceSet#commitment_plan}
        :param cpu_overcommit_ratio: CPU overcommit ratio. Acceptable values are between 1.0 and 2.0 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#cpu_overcommit_ratio MigrationCenterPreferenceSet#cpu_overcommit_ratio}
        :param host_maintenance_policy: Sole Tenancy nodes maintenance policy. Possible values: 'HOST_MAINTENANCE_POLICY_UNSPECIFIED', 'HOST_MAINTENANCE_POLICY_DEFAULT', 'HOST_MAINTENANCE_POLICY_RESTART_IN_PLACE', 'HOST_MAINTENANCE_POLICY_MIGRATE_WITHIN_NODE_GROUP'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#host_maintenance_policy MigrationCenterPreferenceSet#host_maintenance_policy}
        :param node_types: node_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#node_types MigrationCenterPreferenceSet#node_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad4b7901544a77bf32b75f9b7d1dd30ef34a9f011176b0acbf6ef8d1858f7e99)
            check_type(argname="argument commitment_plan", value=commitment_plan, expected_type=type_hints["commitment_plan"])
            check_type(argname="argument cpu_overcommit_ratio", value=cpu_overcommit_ratio, expected_type=type_hints["cpu_overcommit_ratio"])
            check_type(argname="argument host_maintenance_policy", value=host_maintenance_policy, expected_type=type_hints["host_maintenance_policy"])
            check_type(argname="argument node_types", value=node_types, expected_type=type_hints["node_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if commitment_plan is not None:
            self._values["commitment_plan"] = commitment_plan
        if cpu_overcommit_ratio is not None:
            self._values["cpu_overcommit_ratio"] = cpu_overcommit_ratio
        if host_maintenance_policy is not None:
            self._values["host_maintenance_policy"] = host_maintenance_policy
        if node_types is not None:
            self._values["node_types"] = node_types

    @builtins.property
    def commitment_plan(self) -> typing.Optional[builtins.str]:
        '''Commitment plan to consider when calculating costs for virtual machine insights and recommendations.

        If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'ON_DEMAND', 'COMMITMENT_1_YEAR', 'COMMITMENT_3_YEAR'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#commitment_plan MigrationCenterPreferenceSet#commitment_plan}
        '''
        result = self._values.get("commitment_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_overcommit_ratio(self) -> typing.Optional[jsii.Number]:
        '''CPU overcommit ratio. Acceptable values are between 1.0 and 2.0 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#cpu_overcommit_ratio MigrationCenterPreferenceSet#cpu_overcommit_ratio}
        '''
        result = self._values.get("cpu_overcommit_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def host_maintenance_policy(self) -> typing.Optional[builtins.str]:
        '''Sole Tenancy nodes maintenance policy. Possible values: 'HOST_MAINTENANCE_POLICY_UNSPECIFIED', 'HOST_MAINTENANCE_POLICY_DEFAULT', 'HOST_MAINTENANCE_POLICY_RESTART_IN_PLACE', 'HOST_MAINTENANCE_POLICY_MIGRATE_WITHIN_NODE_GROUP'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#host_maintenance_policy MigrationCenterPreferenceSet#host_maintenance_policy}
        '''
        result = self._values.get("host_maintenance_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes"]]]:
        '''node_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#node_types MigrationCenterPreferenceSet#node_types}
        '''
        result = self._values.get("node_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes",
    jsii_struct_bases=[],
    name_mapping={"node_name": "nodeName"},
)
class MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes:
    def __init__(self, *, node_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param node_name: Name of the Sole Tenant node. Consult https://cloud.google.com/compute/docs/nodes/sole-tenant-nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#node_name MigrationCenterPreferenceSet#node_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49fba2d1536f3ad868ffa9748d5b78b843319015f3b27f0284ccb64c001e81d0)
            check_type(argname="argument node_name", value=node_name, expected_type=type_hints["node_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_name is not None:
            self._values["node_name"] = node_name

    @builtins.property
    def node_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Sole Tenant node. Consult https://cloud.google.com/compute/docs/nodes/sole-tenant-nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#node_name MigrationCenterPreferenceSet#node_name}
        '''
        result = self._values.get("node_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d7f2b3d7a0bb528102ed98586ccc514abcd50efe00f01b1a3bf57e809e21cf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e602d669f16c489b812bfc5413c4333b99082b3c65bd43072740af157c402398)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d59b717ea58cea7ddac3001f7072fac920ec3db838f9c23713b199b0f02000)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6896012a0af99c3d0a2234e253cf0fc028164472d69ac68b6239a6d1cf7a2b60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d0036bb5dd06bc81f30bed30687d213f6f34797a2f0b442cfb025a85b427e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea39cbd60ef05b338e9c30ca449912d8e19f02f09adb3419ad8c7402fd86365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc42c671804e2466a4a99667bfa3873826397acda5030721c0f2a0aa9fa1473f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNodeName")
    def reset_node_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeName", []))

    @builtins.property
    @jsii.member(jsii_name="nodeNameInput")
    def node_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeName")
    def node_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeName"))

    @node_name.setter
    def node_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67e0740cad7c0f97de17482bf54734daddcd346df385ea767db0521bf100b840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5a30b9acc67b3b36d02c3cbdca497de09e936865bf6f30c149ff2b71b1a165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a56fc2f9171a259bf1e6f7be8056b3633a29f6a9d30ab0ae9409ca9ba225dc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeTypes")
    def put_node_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097afd5d1f41ca23e6c1c4d6a39509b30dadd0094c7545bae511898ceea5012f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeTypes", [value]))

    @jsii.member(jsii_name="resetCommitmentPlan")
    def reset_commitment_plan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitmentPlan", []))

    @jsii.member(jsii_name="resetCpuOvercommitRatio")
    def reset_cpu_overcommit_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuOvercommitRatio", []))

    @jsii.member(jsii_name="resetHostMaintenancePolicy")
    def reset_host_maintenance_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostMaintenancePolicy", []))

    @jsii.member(jsii_name="resetNodeTypes")
    def reset_node_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeTypes", []))

    @builtins.property
    @jsii.member(jsii_name="nodeTypes")
    def node_types(
        self,
    ) -> MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesList:
        return typing.cast(MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesList, jsii.get(self, "nodeTypes"))

    @builtins.property
    @jsii.member(jsii_name="commitmentPlanInput")
    def commitment_plan_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitmentPlanInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuOvercommitRatioInput")
    def cpu_overcommit_ratio_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuOvercommitRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="hostMaintenancePolicyInput")
    def host_maintenance_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostMaintenancePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypesInput")
    def node_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]], jsii.get(self, "nodeTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="commitmentPlan")
    def commitment_plan(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitmentPlan"))

    @commitment_plan.setter
    def commitment_plan(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09c0da43c71e66f46e18ef8c983778448a65e8169c3bb101ba67b23391b7ea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitmentPlan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuOvercommitRatio")
    def cpu_overcommit_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuOvercommitRatio"))

    @cpu_overcommit_ratio.setter
    def cpu_overcommit_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97b19185f90552ecaa7870aa740008f5cbc816264c0d549107c531147e8d7353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuOvercommitRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostMaintenancePolicy")
    def host_maintenance_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostMaintenancePolicy"))

    @host_maintenance_policy.setter
    def host_maintenance_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86f876bdd4bf78e027ab54935e87400ee8d419f72569c1632049fbb0dedc8075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostMaintenancePolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences]:
        return typing.cast(typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d7d9042eb458901206894bd6c2e0dc921cdf1fba952e6e477732fc38da76805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences",
    jsii_struct_bases=[],
    name_mapping={
        "commitment_plan": "commitmentPlan",
        "cpu_overcommit_ratio": "cpuOvercommitRatio",
        "memory_overcommit_ratio": "memoryOvercommitRatio",
        "storage_deduplication_compression_ratio": "storageDeduplicationCompressionRatio",
    },
)
class MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences:
    def __init__(
        self,
        *,
        commitment_plan: typing.Optional[builtins.str] = None,
        cpu_overcommit_ratio: typing.Optional[jsii.Number] = None,
        memory_overcommit_ratio: typing.Optional[jsii.Number] = None,
        storage_deduplication_compression_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param commitment_plan: Commitment plan to consider when calculating costs for virtual machine insights and recommendations. If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'ON_DEMAND', 'COMMITMENT_1_YEAR_MONTHLY_PAYMENTS', 'COMMITMENT_3_YEAR_MONTHLY_PAYMENTS', 'COMMITMENT_1_YEAR_UPFRONT_PAYMENT', 'COMMITMENT_3_YEAR_UPFRONT_PAYMENT', Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#commitment_plan MigrationCenterPreferenceSet#commitment_plan}
        :param cpu_overcommit_ratio: CPU overcommit ratio. Acceptable values are between 1.0 and 8.0, with 0.1 increment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#cpu_overcommit_ratio MigrationCenterPreferenceSet#cpu_overcommit_ratio}
        :param memory_overcommit_ratio: Memory overcommit ratio. Acceptable values are 1.0, 1.25, 1.5, 1.75 and 2.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#memory_overcommit_ratio MigrationCenterPreferenceSet#memory_overcommit_ratio}
        :param storage_deduplication_compression_ratio: The Deduplication and Compression ratio is based on the logical (Used Before) space required to store data before applying deduplication and compression, in relation to the physical (Used After) space required after applying deduplication and compression. Specifically, the ratio is the Used Before space divided by the Used After space. For example, if the Used Before space is 3 GB, but the physical Used After space is 1 GB, the deduplication and compression ratio is 3x. Acceptable values are between 1.0 and 4.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#storage_deduplication_compression_ratio MigrationCenterPreferenceSet#storage_deduplication_compression_ratio}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55229a87295df635802c8c424300579417e5d8c71471a9a9902f9d1ce776d52)
            check_type(argname="argument commitment_plan", value=commitment_plan, expected_type=type_hints["commitment_plan"])
            check_type(argname="argument cpu_overcommit_ratio", value=cpu_overcommit_ratio, expected_type=type_hints["cpu_overcommit_ratio"])
            check_type(argname="argument memory_overcommit_ratio", value=memory_overcommit_ratio, expected_type=type_hints["memory_overcommit_ratio"])
            check_type(argname="argument storage_deduplication_compression_ratio", value=storage_deduplication_compression_ratio, expected_type=type_hints["storage_deduplication_compression_ratio"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if commitment_plan is not None:
            self._values["commitment_plan"] = commitment_plan
        if cpu_overcommit_ratio is not None:
            self._values["cpu_overcommit_ratio"] = cpu_overcommit_ratio
        if memory_overcommit_ratio is not None:
            self._values["memory_overcommit_ratio"] = memory_overcommit_ratio
        if storage_deduplication_compression_ratio is not None:
            self._values["storage_deduplication_compression_ratio"] = storage_deduplication_compression_ratio

    @builtins.property
    def commitment_plan(self) -> typing.Optional[builtins.str]:
        '''Commitment plan to consider when calculating costs for virtual machine insights and recommendations.

        If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'ON_DEMAND', 'COMMITMENT_1_YEAR_MONTHLY_PAYMENTS', 'COMMITMENT_3_YEAR_MONTHLY_PAYMENTS', 'COMMITMENT_1_YEAR_UPFRONT_PAYMENT', 'COMMITMENT_3_YEAR_UPFRONT_PAYMENT',

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#commitment_plan MigrationCenterPreferenceSet#commitment_plan}
        '''
        result = self._values.get("commitment_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_overcommit_ratio(self) -> typing.Optional[jsii.Number]:
        '''CPU overcommit ratio. Acceptable values are between 1.0 and 8.0, with 0.1 increment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#cpu_overcommit_ratio MigrationCenterPreferenceSet#cpu_overcommit_ratio}
        '''
        result = self._values.get("cpu_overcommit_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_overcommit_ratio(self) -> typing.Optional[jsii.Number]:
        '''Memory overcommit ratio. Acceptable values are 1.0, 1.25, 1.5, 1.75 and 2.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#memory_overcommit_ratio MigrationCenterPreferenceSet#memory_overcommit_ratio}
        '''
        result = self._values.get("memory_overcommit_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_deduplication_compression_ratio(self) -> typing.Optional[jsii.Number]:
        '''The Deduplication and Compression ratio is based on the logical (Used Before) space required to store data before applying deduplication and compression, in relation to the physical (Used After) space required after applying deduplication and compression.

        Specifically, the ratio is the Used Before space divided by the Used After space. For example, if the Used Before space is 3 GB, but the physical Used After space is 1 GB, the deduplication and compression ratio is 3x. Acceptable values are between 1.0 and 4.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/migration_center_preference_set#storage_deduplication_compression_ratio MigrationCenterPreferenceSet#storage_deduplication_compression_ratio}
        '''
        result = self._values.get("storage_deduplication_compression_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.migrationCenterPreferenceSet.MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f972939d58a828fe327125438999945a83789b0add9aefde4f19e9c651eeda17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCommitmentPlan")
    def reset_commitment_plan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitmentPlan", []))

    @jsii.member(jsii_name="resetCpuOvercommitRatio")
    def reset_cpu_overcommit_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuOvercommitRatio", []))

    @jsii.member(jsii_name="resetMemoryOvercommitRatio")
    def reset_memory_overcommit_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryOvercommitRatio", []))

    @jsii.member(jsii_name="resetStorageDeduplicationCompressionRatio")
    def reset_storage_deduplication_compression_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageDeduplicationCompressionRatio", []))

    @builtins.property
    @jsii.member(jsii_name="commitmentPlanInput")
    def commitment_plan_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitmentPlanInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuOvercommitRatioInput")
    def cpu_overcommit_ratio_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuOvercommitRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryOvercommitRatioInput")
    def memory_overcommit_ratio_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryOvercommitRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="storageDeduplicationCompressionRatioInput")
    def storage_deduplication_compression_ratio_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageDeduplicationCompressionRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="commitmentPlan")
    def commitment_plan(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitmentPlan"))

    @commitment_plan.setter
    def commitment_plan(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f042245e48a7c437d7c2fac74202253b601727fe5b49a1126f70993aeb9e3a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitmentPlan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuOvercommitRatio")
    def cpu_overcommit_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuOvercommitRatio"))

    @cpu_overcommit_ratio.setter
    def cpu_overcommit_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c5ec2d9d75b87a65431fb1985aab1c09e1a58a5a5fa65ba403da9fcdeb5540f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuOvercommitRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryOvercommitRatio")
    def memory_overcommit_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryOvercommitRatio"))

    @memory_overcommit_ratio.setter
    def memory_overcommit_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5abddfe9c6b3f6bf6154fda0d30fd47ec5f1875d90c676125c544ca4df958485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryOvercommitRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageDeduplicationCompressionRatio")
    def storage_deduplication_compression_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageDeduplicationCompressionRatio"))

    @storage_deduplication_compression_ratio.setter
    def storage_deduplication_compression_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a57c164c0908fb85546b6c85da693ff8e3b98673d2c35e169b8be4e8d7b5926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageDeduplicationCompressionRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences]:
        return typing.cast(typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900c7e741b3bf6adbff895c8d7800eaeba6d943be77051c836b710254e4f78da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MigrationCenterPreferenceSet",
    "MigrationCenterPreferenceSetConfig",
    "MigrationCenterPreferenceSetTimeouts",
    "MigrationCenterPreferenceSetTimeoutsOutputReference",
    "MigrationCenterPreferenceSetVirtualMachinePreferences",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesList",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesOutputReference",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesOutputReference",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesOutputReference",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesOutputReference",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferencesOutputReference",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesList",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesOutputReference",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesOutputReference",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences",
    "MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferencesOutputReference",
]

publication.publish()

def _typecheckingstub__7f138716ca92b865846b5dcfbfddcc644218b8c1bb069ea8a9eaad6d1734ec5e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    preference_set_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MigrationCenterPreferenceSetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine_preferences: typing.Optional[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferences, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__39b6a621ecf5b1ec3fefc1cd9c08233a5b1ba8afe944e9e4c8521876f8fd2509(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a22af2ca2f609eb6e295fbb98a1410237a7ab4f86a4c70bed2d276c9851d4d4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f632ac1e538ed1e8efc014fcebfb1b8d6ea9306a060dd566d418b611c0ebad5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281aff1a7c1797a7cf0fdf582cbea7fa7cc7f978b590e9fe75fbc625c674f0c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f0e23f023d19fbb7cf0d8807e63c9858d869f7fb648e16d195d43f966f3782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7d13bab51c1fd1f38a10bb963d5d46a3e3240344c8fd030075de0d26e94f23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d09ee579fbf55cf25e6f75b11f329285ac89b3ba00cb68dacc0ba0e1ac31d59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29bc577b313c7cb0292c66faa10d641d6955000546fd0b26bddf60c6bb7a5ec(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    preference_set_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MigrationCenterPreferenceSetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine_preferences: typing.Optional[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferences, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776449334e17d7e5a6b0689bffdef9e9b3ecc7a46b63a861da220273f8a5ed9f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb38dbfb276ba51d6ac74e5856f87e1d6000e22342be720fc0b21ff70853c0f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8494478e9e659c6915067262f7cde9399cb150d591951736f3501e376b81fc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fb08773caa959ba1507cb54590312069171ba593259a12201453df68c12cd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1789e70f4dcc102669202e009abacf47edbfd0332a3550269250c1ce9a75b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2dfd384c10bef3bcd6e42a78f2beb95d2d59db21661b48a3f91bb2cfc1e70cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MigrationCenterPreferenceSetTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5316eb4a0e659e46ff47e27e2e03f89c51c18363812cac045ab1cfd5b07aa5d(
    *,
    commitment_plan: typing.Optional[builtins.str] = None,
    compute_engine_preferences: typing.Optional[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    region_preferences: typing.Optional[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    sizing_optimization_strategy: typing.Optional[builtins.str] = None,
    sole_tenancy_preferences: typing.Optional[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    target_product: typing.Optional[builtins.str] = None,
    vmware_engine_preferences: typing.Optional[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed37e68e07fd090d97e0c3bd9d0574827af665772360aca55160fb104e324d1(
    *,
    license_type: typing.Optional[builtins.str] = None,
    machine_preferences: typing.Optional[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76bd1b748eb66ab025c82b10d352ac1eb4ca9d0df41d8fbc0236670839f6cf0(
    *,
    allowed_machine_series: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed562e28bdbeb2b51f0fcd060a037c19f8d4fa751786dee72d20f14b994382cc(
    *,
    code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2e50095f85abf7187f22c532b5d1d6c7e61e504d86d77b95459b04a5e43da0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b943025d283f3018d7db8f78659f32d62cd70e45d2bb2f295d41d8a3fb9fbc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35eecf8c5e82b52120b4e82b5338b473a99815cbcb5da28ce585675d1b5ed4dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2219d395558a5e1ebf8b41496c2e9ccdfdedb15295569eab485bae7db6e7e5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251eb033e252ae1ef3c7d2a88357fa78c83e94c2b8699643259721de541c6d86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2c615c272616ca4adc326dd65716e2b3a5687b2096df3d4ac46eb0b6209a1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8777157a16cce46977546a191c553f439408fc4b5f838218be4914dbe29dac2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d453855a85325ca63dcc11241deabfbf74a1573dacf67936c417b195a895fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02fbb0382301ceba9a8db12e02ce6459d2945ca49a51ec9de22797468531027(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a943ec54e985294e0331c10980b6ee68d216857c72ecbc3c0da003795c08236e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f0c3649fc6028d7feec078c062cbd1e61bbbe42e1f15fa0632d660108502cd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5fc3080f684c9274045496f91e062cd7e4feea4f6985fdd650befecc90acf7(
    value: typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36c88806c42ffeccb6b331b81e837834f582a467e46012b8e35bdaedb41463f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ac28976997d454341c4012497d6565566085ff2fdbdc17cc39d9d11fb4abb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f1b09805e69cefc2d22a1171df8850812ae79a7fa52d200c417f1d2190ef40(
    value: typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9ad3552fd4426060b07f162faedfa5dbbda3a4c03fe4e5e335afcd480516b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d613230f60f3b10b3b74fab8e59b82169321de1eddd3310c7bae1c66767fe2fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630f5c0f505639026b719b91725b9b89e5c012a4da313b5be3aaa1cb64fe2bd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b44ca312918d6f0dfdd0fbce9b657a52b59080d91f69405236e09a99f9bac85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d19f9c27a62882264100c6f38548e63fa62ed0ca4d23a36988da1abd95e69f3(
    value: typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88c3612465744f8106a2a85f58151c28ebb5e6085f5b0f1053a32fd3fc562bc(
    *,
    preferred_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03267703ce3a5a3e6e31a50f49be4b2e5b1fe6095b28064350c81f95a3fe1b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995282a7df4e61b30e96fb4642b05c75a1a4165c63d61ba8de18a17d7a43d255(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ee77c5f62e1500b1a94124c08a5bdadc70ce79ec001e9358bf3c32656448c9(
    value: typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4b7901544a77bf32b75f9b7d1dd30ef34a9f011176b0acbf6ef8d1858f7e99(
    *,
    commitment_plan: typing.Optional[builtins.str] = None,
    cpu_overcommit_ratio: typing.Optional[jsii.Number] = None,
    host_maintenance_policy: typing.Optional[builtins.str] = None,
    node_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49fba2d1536f3ad868ffa9748d5b78b843319015f3b27f0284ccb64c001e81d0(
    *,
    node_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7f2b3d7a0bb528102ed98586ccc514abcd50efe00f01b1a3bf57e809e21cf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e602d669f16c489b812bfc5413c4333b99082b3c65bd43072740af157c402398(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d59b717ea58cea7ddac3001f7072fac920ec3db838f9c23713b199b0f02000(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6896012a0af99c3d0a2234e253cf0fc028164472d69ac68b6239a6d1cf7a2b60(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0036bb5dd06bc81f30bed30687d213f6f34797a2f0b442cfb025a85b427e0a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea39cbd60ef05b338e9c30ca449912d8e19f02f09adb3419ad8c7402fd86365(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc42c671804e2466a4a99667bfa3873826397acda5030721c0f2a0aa9fa1473f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e0740cad7c0f97de17482bf54734daddcd346df385ea767db0521bf100b840(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5a30b9acc67b3b36d02c3cbdca497de09e936865bf6f30c149ff2b71b1a165(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a56fc2f9171a259bf1e6f7be8056b3633a29f6a9d30ab0ae9409ca9ba225dc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097afd5d1f41ca23e6c1c4d6a39509b30dadd0094c7545bae511898ceea5012f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09c0da43c71e66f46e18ef8c983778448a65e8169c3bb101ba67b23391b7ea4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97b19185f90552ecaa7870aa740008f5cbc816264c0d549107c531147e8d7353(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f876bdd4bf78e027ab54935e87400ee8d419f72569c1632049fbb0dedc8075(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7d9042eb458901206894bd6c2e0dc921cdf1fba952e6e477732fc38da76805(
    value: typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55229a87295df635802c8c424300579417e5d8c71471a9a9902f9d1ce776d52(
    *,
    commitment_plan: typing.Optional[builtins.str] = None,
    cpu_overcommit_ratio: typing.Optional[jsii.Number] = None,
    memory_overcommit_ratio: typing.Optional[jsii.Number] = None,
    storage_deduplication_compression_ratio: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f972939d58a828fe327125438999945a83789b0add9aefde4f19e9c651eeda17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f042245e48a7c437d7c2fac74202253b601727fe5b49a1126f70993aeb9e3a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5ec2d9d75b87a65431fb1985aab1c09e1a58a5a5fa65ba403da9fcdeb5540f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abddfe9c6b3f6bf6154fda0d30fd47ec5f1875d90c676125c544ca4df958485(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a57c164c0908fb85546b6c85da693ff8e3b98673d2c35e169b8be4e8d7b5926(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900c7e741b3bf6adbff895c8d7800eaeba6d943be77051c836b710254e4f78da(
    value: typing.Optional[MigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences],
) -> None:
    """Type checking stubs"""
    pass
