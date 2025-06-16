r'''
# `google_migration_center_preference_set`

Refer to the Terraform Registry for docs: [`google_migration_center_preference_set`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set).
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


class GoogleMigrationCenterPreferenceSet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSet",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set google_migration_center_preference_set}.'''

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
        timeouts: typing.Optional[typing.Union["GoogleMigrationCenterPreferenceSetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine_preferences: typing.Optional[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set google_migration_center_preference_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Part of 'parent'. See documentation of 'projectsId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#location GoogleMigrationCenterPreferenceSet#location}
        :param preference_set_id: Required. User specified ID for the preference set. It will become the last component of the preference set name. The ID must be unique within the project, must conform with RFC-1034, is restricted to lower-cased letters, and has a maximum length of 63 characters. The ID must match the regular expression '`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#preference_set_id GoogleMigrationCenterPreferenceSet#preference_set_id}
        :param description: A description of the preference set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#description GoogleMigrationCenterPreferenceSet#description}
        :param display_name: User-friendly display name. Maximum length is 63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#display_name GoogleMigrationCenterPreferenceSet#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#id GoogleMigrationCenterPreferenceSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#project GoogleMigrationCenterPreferenceSet#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#timeouts GoogleMigrationCenterPreferenceSet#timeouts}
        :param virtual_machine_preferences: virtual_machine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#virtual_machine_preferences GoogleMigrationCenterPreferenceSet#virtual_machine_preferences}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38fe156dc34a01aba4cb2e32de7788746738d0c55835cdef438d5cb9dce84397)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleMigrationCenterPreferenceSetConfig(
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
        '''Generates CDKTF code for importing a GoogleMigrationCenterPreferenceSet resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleMigrationCenterPreferenceSet to import.
        :param import_from_id: The id of the existing GoogleMigrationCenterPreferenceSet that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleMigrationCenterPreferenceSet to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8920ab546e3f688af88335825811b6426bd9debc453e48356f41f483de43846)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#create GoogleMigrationCenterPreferenceSet#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#delete GoogleMigrationCenterPreferenceSet#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#update GoogleMigrationCenterPreferenceSet#update}.
        '''
        value = GoogleMigrationCenterPreferenceSetTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualMachinePreferences")
    def put_virtual_machine_preferences(
        self,
        *,
        commitment_plan: typing.Optional[builtins.str] = None,
        compute_engine_preferences: typing.Optional[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        region_preferences: typing.Optional[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        sizing_optimization_strategy: typing.Optional[builtins.str] = None,
        sole_tenancy_preferences: typing.Optional[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        target_product: typing.Optional[builtins.str] = None,
        vmware_engine_preferences: typing.Optional[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param commitment_plan: Commitment plan to consider when calculating costs for virtual machine insights and recommendations. If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'COMMITMENT_PLAN_NONE', 'COMMITMENT_PLAN_ONE_YEAR', 'COMMITMENT_PLAN_THREE_YEARS' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#commitment_plan GoogleMigrationCenterPreferenceSet#commitment_plan}
        :param compute_engine_preferences: compute_engine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#compute_engine_preferences GoogleMigrationCenterPreferenceSet#compute_engine_preferences}
        :param region_preferences: region_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#region_preferences GoogleMigrationCenterPreferenceSet#region_preferences}
        :param sizing_optimization_strategy: Sizing optimization strategy specifies the preferred strategy used when extrapolating usage data to calculate insights and recommendations for a virtual machine. If you are unsure which value to set, a moderate sizing optimization strategy is often a good value to start with. Possible values: 'SIZING_OPTIMIZATION_STRATEGY_UNSPECIFIED', 'SIZING_OPTIMIZATION_STRATEGY_SAME_AS_SOURCE', 'SIZING_OPTIMIZATION_STRATEGY_MODERATE', 'SIZING_OPTIMIZATION_STRATEGY_AGGRESSIVE' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#sizing_optimization_strategy GoogleMigrationCenterPreferenceSet#sizing_optimization_strategy}
        :param sole_tenancy_preferences: sole_tenancy_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#sole_tenancy_preferences GoogleMigrationCenterPreferenceSet#sole_tenancy_preferences}
        :param target_product: Target product for assets using this preference set. Specify either target product or business goal, but not both. Possible values: 'COMPUTE_MIGRATION_TARGET_PRODUCT_UNSPECIFIED', 'COMPUTE_MIGRATION_TARGET_PRODUCT_COMPUTE_ENGINE', 'COMPUTE_MIGRATION_TARGET_PRODUCT_VMWARE_ENGINE', 'COMPUTE_MIGRATION_TARGET_PRODUCT_SOLE_TENANCY' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#target_product GoogleMigrationCenterPreferenceSet#target_product}
        :param vmware_engine_preferences: vmware_engine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#vmware_engine_preferences GoogleMigrationCenterPreferenceSet#vmware_engine_preferences}
        '''
        value = GoogleMigrationCenterPreferenceSetVirtualMachinePreferences(
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
    def timeouts(self) -> "GoogleMigrationCenterPreferenceSetTimeoutsOutputReference":
        return typing.cast("GoogleMigrationCenterPreferenceSetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachinePreferences")
    def virtual_machine_preferences(
        self,
    ) -> "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesOutputReference":
        return typing.cast("GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesOutputReference", jsii.get(self, "virtualMachinePreferences"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleMigrationCenterPreferenceSetTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleMigrationCenterPreferenceSetTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachinePreferencesInput")
    def virtual_machine_preferences_input(
        self,
    ) -> typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferences"]:
        return typing.cast(typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferences"], jsii.get(self, "virtualMachinePreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467ffb7752f95c0f6a1ca1a87368576403edf9e9d56250d81becb6aa410648fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42d31200871f5bcbb432e5b1de8f19250d62e3fbd855aca4ad73c34948d0eb71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078f7008787769fe51ca2d90b019fee75e08e4e9eed5cb8afc88c6b9e33bfe22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776b1c017f9c92ed67b6564b4149a40ba01a997e10876a36fec9852cd0736630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferenceSetId")
    def preference_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferenceSetId"))

    @preference_set_id.setter
    def preference_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__808ec2c4a7e049b5f4b61c2e4ac1e5e46d4ef4989831f32519656b3fa816af6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferenceSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7241958697e27d50dcdf817f0f9a61f2647bfb2282c7388146a7dddfc4b12df1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetConfig",
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
class GoogleMigrationCenterPreferenceSetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        timeouts: typing.Optional[typing.Union["GoogleMigrationCenterPreferenceSetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine_preferences: typing.Optional[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Part of 'parent'. See documentation of 'projectsId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#location GoogleMigrationCenterPreferenceSet#location}
        :param preference_set_id: Required. User specified ID for the preference set. It will become the last component of the preference set name. The ID must be unique within the project, must conform with RFC-1034, is restricted to lower-cased letters, and has a maximum length of 63 characters. The ID must match the regular expression '`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#preference_set_id GoogleMigrationCenterPreferenceSet#preference_set_id}
        :param description: A description of the preference set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#description GoogleMigrationCenterPreferenceSet#description}
        :param display_name: User-friendly display name. Maximum length is 63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#display_name GoogleMigrationCenterPreferenceSet#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#id GoogleMigrationCenterPreferenceSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#project GoogleMigrationCenterPreferenceSet#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#timeouts GoogleMigrationCenterPreferenceSet#timeouts}
        :param virtual_machine_preferences: virtual_machine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#virtual_machine_preferences GoogleMigrationCenterPreferenceSet#virtual_machine_preferences}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleMigrationCenterPreferenceSetTimeouts(**timeouts)
        if isinstance(virtual_machine_preferences, dict):
            virtual_machine_preferences = GoogleMigrationCenterPreferenceSetVirtualMachinePreferences(**virtual_machine_preferences)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c87d512ef836b9eeac03fc146891ae97922be320bad4ee7e13869efe54ca25)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#location GoogleMigrationCenterPreferenceSet#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def preference_set_id(self) -> builtins.str:
        '''Required.

        User specified ID for the preference set. It will become the last component of the preference set name. The ID must be unique within the project, must conform with RFC-1034, is restricted to lower-cased letters, and has a maximum length of 63 characters. The ID must match the regular expression '`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#preference_set_id GoogleMigrationCenterPreferenceSet#preference_set_id}
        '''
        result = self._values.get("preference_set_id")
        assert result is not None, "Required property 'preference_set_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the preference set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#description GoogleMigrationCenterPreferenceSet#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User-friendly display name. Maximum length is 63 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#display_name GoogleMigrationCenterPreferenceSet#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#id GoogleMigrationCenterPreferenceSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#project GoogleMigrationCenterPreferenceSet#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleMigrationCenterPreferenceSetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#timeouts GoogleMigrationCenterPreferenceSet#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleMigrationCenterPreferenceSetTimeouts"], result)

    @builtins.property
    def virtual_machine_preferences(
        self,
    ) -> typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferences"]:
        '''virtual_machine_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#virtual_machine_preferences GoogleMigrationCenterPreferenceSet#virtual_machine_preferences}
        '''
        result = self._values.get("virtual_machine_preferences")
        return typing.cast(typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferences"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMigrationCenterPreferenceSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleMigrationCenterPreferenceSetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#create GoogleMigrationCenterPreferenceSet#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#delete GoogleMigrationCenterPreferenceSet#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#update GoogleMigrationCenterPreferenceSet#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8339eb1110abfafa8d871ef6d453f37ff8e1647ce2eaafc2d602f49a1b7c4be9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#create GoogleMigrationCenterPreferenceSet#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#delete GoogleMigrationCenterPreferenceSet#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#update GoogleMigrationCenterPreferenceSet#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMigrationCenterPreferenceSetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMigrationCenterPreferenceSetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f018a03538f683b2f4331a5e60a1c1ecc3a22703185cae9a38e763e52c74374)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2099be04d97870fcaf843b2434147458e760f8359200d630eaa0926e2dbb955)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ee5ccf811e44e016e76a99dea044f252ebd1032d62a3f6364e717f4c198460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c36ef6993f9be5372c3280bb2e7056de272ba11532dede78ff72075878c263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMigrationCenterPreferenceSetTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMigrationCenterPreferenceSetTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMigrationCenterPreferenceSetTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf32b6cea28acd90b080be130b07ce6149a36edfd1eaca8c72d1bfa9e7a5345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferences",
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
class GoogleMigrationCenterPreferenceSetVirtualMachinePreferences:
    def __init__(
        self,
        *,
        commitment_plan: typing.Optional[builtins.str] = None,
        compute_engine_preferences: typing.Optional[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        region_preferences: typing.Optional[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        sizing_optimization_strategy: typing.Optional[builtins.str] = None,
        sole_tenancy_preferences: typing.Optional[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        target_product: typing.Optional[builtins.str] = None,
        vmware_engine_preferences: typing.Optional[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param commitment_plan: Commitment plan to consider when calculating costs for virtual machine insights and recommendations. If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'COMMITMENT_PLAN_NONE', 'COMMITMENT_PLAN_ONE_YEAR', 'COMMITMENT_PLAN_THREE_YEARS' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#commitment_plan GoogleMigrationCenterPreferenceSet#commitment_plan}
        :param compute_engine_preferences: compute_engine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#compute_engine_preferences GoogleMigrationCenterPreferenceSet#compute_engine_preferences}
        :param region_preferences: region_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#region_preferences GoogleMigrationCenterPreferenceSet#region_preferences}
        :param sizing_optimization_strategy: Sizing optimization strategy specifies the preferred strategy used when extrapolating usage data to calculate insights and recommendations for a virtual machine. If you are unsure which value to set, a moderate sizing optimization strategy is often a good value to start with. Possible values: 'SIZING_OPTIMIZATION_STRATEGY_UNSPECIFIED', 'SIZING_OPTIMIZATION_STRATEGY_SAME_AS_SOURCE', 'SIZING_OPTIMIZATION_STRATEGY_MODERATE', 'SIZING_OPTIMIZATION_STRATEGY_AGGRESSIVE' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#sizing_optimization_strategy GoogleMigrationCenterPreferenceSet#sizing_optimization_strategy}
        :param sole_tenancy_preferences: sole_tenancy_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#sole_tenancy_preferences GoogleMigrationCenterPreferenceSet#sole_tenancy_preferences}
        :param target_product: Target product for assets using this preference set. Specify either target product or business goal, but not both. Possible values: 'COMPUTE_MIGRATION_TARGET_PRODUCT_UNSPECIFIED', 'COMPUTE_MIGRATION_TARGET_PRODUCT_COMPUTE_ENGINE', 'COMPUTE_MIGRATION_TARGET_PRODUCT_VMWARE_ENGINE', 'COMPUTE_MIGRATION_TARGET_PRODUCT_SOLE_TENANCY' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#target_product GoogleMigrationCenterPreferenceSet#target_product}
        :param vmware_engine_preferences: vmware_engine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#vmware_engine_preferences GoogleMigrationCenterPreferenceSet#vmware_engine_preferences}
        '''
        if isinstance(compute_engine_preferences, dict):
            compute_engine_preferences = GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences(**compute_engine_preferences)
        if isinstance(region_preferences, dict):
            region_preferences = GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences(**region_preferences)
        if isinstance(sole_tenancy_preferences, dict):
            sole_tenancy_preferences = GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences(**sole_tenancy_preferences)
        if isinstance(vmware_engine_preferences, dict):
            vmware_engine_preferences = GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences(**vmware_engine_preferences)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c1946ac0d17ac03ab38029e111f4a9a4d3da98ee6af26b90c8160e2f87a4bf)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#commitment_plan GoogleMigrationCenterPreferenceSet#commitment_plan}
        '''
        result = self._values.get("commitment_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_engine_preferences(
        self,
    ) -> typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences"]:
        '''compute_engine_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#compute_engine_preferences GoogleMigrationCenterPreferenceSet#compute_engine_preferences}
        '''
        result = self._values.get("compute_engine_preferences")
        return typing.cast(typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences"], result)

    @builtins.property
    def region_preferences(
        self,
    ) -> typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences"]:
        '''region_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#region_preferences GoogleMigrationCenterPreferenceSet#region_preferences}
        '''
        result = self._values.get("region_preferences")
        return typing.cast(typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences"], result)

    @builtins.property
    def sizing_optimization_strategy(self) -> typing.Optional[builtins.str]:
        '''Sizing optimization strategy specifies the preferred strategy used when extrapolating usage data to calculate insights and recommendations for a virtual machine.

        If you are unsure which value to set, a moderate sizing optimization strategy is often a good value to start with. Possible values: 'SIZING_OPTIMIZATION_STRATEGY_UNSPECIFIED', 'SIZING_OPTIMIZATION_STRATEGY_SAME_AS_SOURCE', 'SIZING_OPTIMIZATION_STRATEGY_MODERATE', 'SIZING_OPTIMIZATION_STRATEGY_AGGRESSIVE'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#sizing_optimization_strategy GoogleMigrationCenterPreferenceSet#sizing_optimization_strategy}
        '''
        result = self._values.get("sizing_optimization_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sole_tenancy_preferences(
        self,
    ) -> typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences"]:
        '''sole_tenancy_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#sole_tenancy_preferences GoogleMigrationCenterPreferenceSet#sole_tenancy_preferences}
        '''
        result = self._values.get("sole_tenancy_preferences")
        return typing.cast(typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences"], result)

    @builtins.property
    def target_product(self) -> typing.Optional[builtins.str]:
        '''Target product for assets using this preference set.

        Specify either target product or business goal, but not both. Possible values: 'COMPUTE_MIGRATION_TARGET_PRODUCT_UNSPECIFIED', 'COMPUTE_MIGRATION_TARGET_PRODUCT_COMPUTE_ENGINE', 'COMPUTE_MIGRATION_TARGET_PRODUCT_VMWARE_ENGINE', 'COMPUTE_MIGRATION_TARGET_PRODUCT_SOLE_TENANCY'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#target_product GoogleMigrationCenterPreferenceSet#target_product}
        '''
        result = self._values.get("target_product")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vmware_engine_preferences(
        self,
    ) -> typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences"]:
        '''vmware_engine_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#vmware_engine_preferences GoogleMigrationCenterPreferenceSet#vmware_engine_preferences}
        '''
        result = self._values.get("vmware_engine_preferences")
        return typing.cast(typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMigrationCenterPreferenceSetVirtualMachinePreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences",
    jsii_struct_bases=[],
    name_mapping={
        "license_type": "licenseType",
        "machine_preferences": "machinePreferences",
    },
)
class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences:
    def __init__(
        self,
        *,
        license_type: typing.Optional[builtins.str] = None,
        machine_preferences: typing.Optional[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param license_type: License type to consider when calculating costs for virtual machine insights and recommendations. If unspecified, costs are calculated based on the default licensing plan. Possible values: 'LICENSE_TYPE_UNSPECIFIED', 'LICENSE_TYPE_DEFAULT', 'LICENSE_TYPE_BRING_YOUR_OWN_LICENSE' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#license_type GoogleMigrationCenterPreferenceSet#license_type}
        :param machine_preferences: machine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#machine_preferences GoogleMigrationCenterPreferenceSet#machine_preferences}
        '''
        if isinstance(machine_preferences, dict):
            machine_preferences = GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences(**machine_preferences)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f79c7d90f2188df5b7160679d5997d8cb6d7e1a7ebe0e47a15b8bc597221ef35)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#license_type GoogleMigrationCenterPreferenceSet#license_type}
        '''
        result = self._values.get("license_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_preferences(
        self,
    ) -> typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences"]:
        '''machine_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#machine_preferences GoogleMigrationCenterPreferenceSet#machine_preferences}
        '''
        result = self._values.get("machine_preferences")
        return typing.cast(typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences",
    jsii_struct_bases=[],
    name_mapping={"allowed_machine_series": "allowedMachineSeries"},
)
class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences:
    def __init__(
        self,
        *,
        allowed_machine_series: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_machine_series: allowed_machine_series block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#allowed_machine_series GoogleMigrationCenterPreferenceSet#allowed_machine_series}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ea3a5e20e1f881bdc452e61c62303e2af805effcd931ed65fa40eb0f536c7f)
            check_type(argname="argument allowed_machine_series", value=allowed_machine_series, expected_type=type_hints["allowed_machine_series"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_machine_series is not None:
            self._values["allowed_machine_series"] = allowed_machine_series

    @builtins.property
    def allowed_machine_series(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries"]]]:
        '''allowed_machine_series block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#allowed_machine_series GoogleMigrationCenterPreferenceSet#allowed_machine_series}
        '''
        result = self._values.get("allowed_machine_series")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries",
    jsii_struct_bases=[],
    name_mapping={"code": "code"},
)
class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries:
    def __init__(self, *, code: typing.Optional[builtins.str] = None) -> None:
        '''
        :param code: Code to identify a Compute Engine machine series. Consult https://cloud.google.com/compute/docs/machine-resource#machine_type_comparison for more details on the available series. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#code GoogleMigrationCenterPreferenceSet#code}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d21d9dff74f23b97bb7f94e294f5cab555f0b23463cc5843502001240842ed)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code is not None:
            self._values["code"] = code

    @builtins.property
    def code(self) -> typing.Optional[builtins.str]:
        '''Code to identify a Compute Engine machine series. Consult https://cloud.google.com/compute/docs/machine-resource#machine_type_comparison for more details on the available series.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#code GoogleMigrationCenterPreferenceSet#code}
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aec6fb6b76b66571683d441533f11352d6cc10960208a9feabdef26257b36cf1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e542cbd94528e01e64c87fd0ccf95891340a2602f1b1bd67f78116962e8bdd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f353168a2dda1096a1dfde6abe0275145b61e356529a9b607a3d1f4467df00a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72ed5ba008dcae85874b0b69f1856ab255473fd67a57a128c7f93d9df5f3ff4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3342eb9fc3da3482e6a14bac253030f1d95993e31e963ebf9d4118e1d5a5b282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d72ae686bbf17940d1fcbbebe047aa6ddc751f9e0fdd6704cf3e0c8f1fa5b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ea012cb694343af7edc4856f5d8832b9300b74aba6f1d1f95e9e50fd9bc5131)
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
            type_hints = typing.get_type_hints(_typecheckingstub__947b62e94650555f1810eab361e653a2a2d0b409247b94f75721c2cd966533b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442a2265786688e7d9953c772911c3dadcc473a369d9a525af50dad0a24676bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54de2a7ce012d0f37710e89b87d1dfffe710818cd5c624bbd9eb18dd03fc4d8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllowedMachineSeries")
    def put_allowed_machine_series(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdb7db1bafe9d13112d441b81b40fd511a7a4dd61595603b8371e666d449053b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedMachineSeries", [value]))

    @jsii.member(jsii_name="resetAllowedMachineSeries")
    def reset_allowed_machine_series(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedMachineSeries", []))

    @builtins.property
    @jsii.member(jsii_name="allowedMachineSeries")
    def allowed_machine_series(
        self,
    ) -> GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesList:
        return typing.cast(GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesList, jsii.get(self, "allowedMachineSeries"))

    @builtins.property
    @jsii.member(jsii_name="allowedMachineSeriesInput")
    def allowed_machine_series_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]], jsii.get(self, "allowedMachineSeriesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences]:
        return typing.cast(typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd95e222530a82940e9f95c8d1b145a32ea909005dded010dd25b08d22dcecb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d96d60a7da74070bf67c572d448305cb17714136779ddb3721c1520b1c806c76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMachinePreferences")
    def put_machine_preferences(
        self,
        *,
        allowed_machine_series: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_machine_series: allowed_machine_series block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#allowed_machine_series GoogleMigrationCenterPreferenceSet#allowed_machine_series}
        '''
        value = GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences(
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
    ) -> GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesOutputReference:
        return typing.cast(GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesOutputReference, jsii.get(self, "machinePreferences"))

    @builtins.property
    @jsii.member(jsii_name="licenseTypeInput")
    def license_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="machinePreferencesInput")
    def machine_preferences_input(
        self,
    ) -> typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences]:
        return typing.cast(typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences], jsii.get(self, "machinePreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseType")
    def license_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseType"))

    @license_type.setter
    def license_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa97ac32367cbb60bab480e9a9a5ff4cf652dbabb46ced3390d9b606cda39227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences]:
        return typing.cast(typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df787470074e8f94dac2d571c84f383b49160df5b2dcffe2b4689de806ddad06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7e5ff7988c86491ded9c4837efa923ebea686e5b0761c465e2e4cbc822c95ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putComputeEnginePreferences")
    def put_compute_engine_preferences(
        self,
        *,
        license_type: typing.Optional[builtins.str] = None,
        machine_preferences: typing.Optional[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param license_type: License type to consider when calculating costs for virtual machine insights and recommendations. If unspecified, costs are calculated based on the default licensing plan. Possible values: 'LICENSE_TYPE_UNSPECIFIED', 'LICENSE_TYPE_DEFAULT', 'LICENSE_TYPE_BRING_YOUR_OWN_LICENSE' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#license_type GoogleMigrationCenterPreferenceSet#license_type}
        :param machine_preferences: machine_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#machine_preferences GoogleMigrationCenterPreferenceSet#machine_preferences}
        '''
        value = GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences(
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
        :param preferred_regions: A list of preferred regions, ordered by the most preferred region first. Set only valid Google Cloud region names. See https://cloud.google.com/compute/docs/regions-zones for available regions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#preferred_regions GoogleMigrationCenterPreferenceSet#preferred_regions}
        '''
        value = GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences(
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
        node_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param commitment_plan: Commitment plan to consider when calculating costs for virtual machine insights and recommendations. If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'ON_DEMAND', 'COMMITMENT_1_YEAR', 'COMMITMENT_3_YEAR' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#commitment_plan GoogleMigrationCenterPreferenceSet#commitment_plan}
        :param cpu_overcommit_ratio: CPU overcommit ratio. Acceptable values are between 1.0 and 2.0 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#cpu_overcommit_ratio GoogleMigrationCenterPreferenceSet#cpu_overcommit_ratio}
        :param host_maintenance_policy: Sole Tenancy nodes maintenance policy. Possible values: 'HOST_MAINTENANCE_POLICY_UNSPECIFIED', 'HOST_MAINTENANCE_POLICY_DEFAULT', 'HOST_MAINTENANCE_POLICY_RESTART_IN_PLACE', 'HOST_MAINTENANCE_POLICY_MIGRATE_WITHIN_NODE_GROUP'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#host_maintenance_policy GoogleMigrationCenterPreferenceSet#host_maintenance_policy}
        :param node_types: node_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#node_types GoogleMigrationCenterPreferenceSet#node_types}
        '''
        value = GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences(
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
        :param commitment_plan: Commitment plan to consider when calculating costs for virtual machine insights and recommendations. If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'ON_DEMAND', 'COMMITMENT_1_YEAR_MONTHLY_PAYMENTS', 'COMMITMENT_3_YEAR_MONTHLY_PAYMENTS', 'COMMITMENT_1_YEAR_UPFRONT_PAYMENT', 'COMMITMENT_3_YEAR_UPFRONT_PAYMENT', Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#commitment_plan GoogleMigrationCenterPreferenceSet#commitment_plan}
        :param cpu_overcommit_ratio: CPU overcommit ratio. Acceptable values are between 1.0 and 8.0, with 0.1 increment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#cpu_overcommit_ratio GoogleMigrationCenterPreferenceSet#cpu_overcommit_ratio}
        :param memory_overcommit_ratio: Memory overcommit ratio. Acceptable values are 1.0, 1.25, 1.5, 1.75 and 2.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#memory_overcommit_ratio GoogleMigrationCenterPreferenceSet#memory_overcommit_ratio}
        :param storage_deduplication_compression_ratio: The Deduplication and Compression ratio is based on the logical (Used Before) space required to store data before applying deduplication and compression, in relation to the physical (Used After) space required after applying deduplication and compression. Specifically, the ratio is the Used Before space divided by the Used After space. For example, if the Used Before space is 3 GB, but the physical Used After space is 1 GB, the deduplication and compression ratio is 3x. Acceptable values are between 1.0 and 4.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#storage_deduplication_compression_ratio GoogleMigrationCenterPreferenceSet#storage_deduplication_compression_ratio}
        '''
        value = GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences(
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
    ) -> GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesOutputReference:
        return typing.cast(GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesOutputReference, jsii.get(self, "computeEnginePreferences"))

    @builtins.property
    @jsii.member(jsii_name="regionPreferences")
    def region_preferences(
        self,
    ) -> "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferencesOutputReference":
        return typing.cast("GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferencesOutputReference", jsii.get(self, "regionPreferences"))

    @builtins.property
    @jsii.member(jsii_name="soleTenancyPreferences")
    def sole_tenancy_preferences(
        self,
    ) -> "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesOutputReference":
        return typing.cast("GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesOutputReference", jsii.get(self, "soleTenancyPreferences"))

    @builtins.property
    @jsii.member(jsii_name="vmwareEnginePreferences")
    def vmware_engine_preferences(
        self,
    ) -> "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferencesOutputReference":
        return typing.cast("GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferencesOutputReference", jsii.get(self, "vmwareEnginePreferences"))

    @builtins.property
    @jsii.member(jsii_name="commitmentPlanInput")
    def commitment_plan_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitmentPlanInput"))

    @builtins.property
    @jsii.member(jsii_name="computeEnginePreferencesInput")
    def compute_engine_preferences_input(
        self,
    ) -> typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences]:
        return typing.cast(typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences], jsii.get(self, "computeEnginePreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="regionPreferencesInput")
    def region_preferences_input(
        self,
    ) -> typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences"]:
        return typing.cast(typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences"], jsii.get(self, "regionPreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="sizingOptimizationStrategyInput")
    def sizing_optimization_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizingOptimizationStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="soleTenancyPreferencesInput")
    def sole_tenancy_preferences_input(
        self,
    ) -> typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences"]:
        return typing.cast(typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences"], jsii.get(self, "soleTenancyPreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetProductInput")
    def target_product_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetProductInput"))

    @builtins.property
    @jsii.member(jsii_name="vmwareEnginePreferencesInput")
    def vmware_engine_preferences_input(
        self,
    ) -> typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences"]:
        return typing.cast(typing.Optional["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences"], jsii.get(self, "vmwareEnginePreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="commitmentPlan")
    def commitment_plan(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitmentPlan"))

    @commitment_plan.setter
    def commitment_plan(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc8cf0df83de018484b193e9cec318b2de305b597c3bc6c6b6fdb1cd1cea7b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitmentPlan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizingOptimizationStrategy")
    def sizing_optimization_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizingOptimizationStrategy"))

    @sizing_optimization_strategy.setter
    def sizing_optimization_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__654fec476729e887207499224ca1ebf978ab6321904951f5774d5011d22c9d58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizingOptimizationStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetProduct")
    def target_product(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetProduct"))

    @target_product.setter
    def target_product(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f56cfa109a69e2062dd97cc79ac3bde934d1126d5350dd744c39c517edfd36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetProduct", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferences]:
        return typing.cast(typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__658782bc3cba5fa95dd561770b9dde3832d1f16e24ede90cefe46805ae2c6f9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences",
    jsii_struct_bases=[],
    name_mapping={"preferred_regions": "preferredRegions"},
)
class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences:
    def __init__(
        self,
        *,
        preferred_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param preferred_regions: A list of preferred regions, ordered by the most preferred region first. Set only valid Google Cloud region names. See https://cloud.google.com/compute/docs/regions-zones for available regions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#preferred_regions GoogleMigrationCenterPreferenceSet#preferred_regions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd85b9016875e03ab8dbdba30e86b23442d367d79689e9ddc2327f5f5615f412)
            check_type(argname="argument preferred_regions", value=preferred_regions, expected_type=type_hints["preferred_regions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if preferred_regions is not None:
            self._values["preferred_regions"] = preferred_regions

    @builtins.property
    def preferred_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of preferred regions, ordered by the most preferred region first.

        Set only valid Google Cloud region names. See https://cloud.google.com/compute/docs/regions-zones for available regions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#preferred_regions GoogleMigrationCenterPreferenceSet#preferred_regions}
        '''
        result = self._values.get("preferred_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__714572eb257f0791d7c225bf9dfc20cc2aeb062ac1239e05712d275445a420fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f79f5ded86b746749a895dca8da32f0ab14ac7e980e86ef4b629a8f43af40011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences]:
        return typing.cast(typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e881972931596f304d618d62da95d89b5e92dca5dd6e1e9a2f992ef6ad6c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences",
    jsii_struct_bases=[],
    name_mapping={
        "commitment_plan": "commitmentPlan",
        "cpu_overcommit_ratio": "cpuOvercommitRatio",
        "host_maintenance_policy": "hostMaintenancePolicy",
        "node_types": "nodeTypes",
    },
)
class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences:
    def __init__(
        self,
        *,
        commitment_plan: typing.Optional[builtins.str] = None,
        cpu_overcommit_ratio: typing.Optional[jsii.Number] = None,
        host_maintenance_policy: typing.Optional[builtins.str] = None,
        node_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param commitment_plan: Commitment plan to consider when calculating costs for virtual machine insights and recommendations. If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'ON_DEMAND', 'COMMITMENT_1_YEAR', 'COMMITMENT_3_YEAR' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#commitment_plan GoogleMigrationCenterPreferenceSet#commitment_plan}
        :param cpu_overcommit_ratio: CPU overcommit ratio. Acceptable values are between 1.0 and 2.0 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#cpu_overcommit_ratio GoogleMigrationCenterPreferenceSet#cpu_overcommit_ratio}
        :param host_maintenance_policy: Sole Tenancy nodes maintenance policy. Possible values: 'HOST_MAINTENANCE_POLICY_UNSPECIFIED', 'HOST_MAINTENANCE_POLICY_DEFAULT', 'HOST_MAINTENANCE_POLICY_RESTART_IN_PLACE', 'HOST_MAINTENANCE_POLICY_MIGRATE_WITHIN_NODE_GROUP'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#host_maintenance_policy GoogleMigrationCenterPreferenceSet#host_maintenance_policy}
        :param node_types: node_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#node_types GoogleMigrationCenterPreferenceSet#node_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c14c38769da22c8dee6f16aa929b50dbf1d917fc3ac066fd6a9425218279f983)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#commitment_plan GoogleMigrationCenterPreferenceSet#commitment_plan}
        '''
        result = self._values.get("commitment_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_overcommit_ratio(self) -> typing.Optional[jsii.Number]:
        '''CPU overcommit ratio. Acceptable values are between 1.0 and 2.0 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#cpu_overcommit_ratio GoogleMigrationCenterPreferenceSet#cpu_overcommit_ratio}
        '''
        result = self._values.get("cpu_overcommit_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def host_maintenance_policy(self) -> typing.Optional[builtins.str]:
        '''Sole Tenancy nodes maintenance policy. Possible values: 'HOST_MAINTENANCE_POLICY_UNSPECIFIED', 'HOST_MAINTENANCE_POLICY_DEFAULT', 'HOST_MAINTENANCE_POLICY_RESTART_IN_PLACE', 'HOST_MAINTENANCE_POLICY_MIGRATE_WITHIN_NODE_GROUP'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#host_maintenance_policy GoogleMigrationCenterPreferenceSet#host_maintenance_policy}
        '''
        result = self._values.get("host_maintenance_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes"]]]:
        '''node_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#node_types GoogleMigrationCenterPreferenceSet#node_types}
        '''
        result = self._values.get("node_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes",
    jsii_struct_bases=[],
    name_mapping={"node_name": "nodeName"},
)
class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes:
    def __init__(self, *, node_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param node_name: Name of the Sole Tenant node. Consult https://cloud.google.com/compute/docs/nodes/sole-tenant-nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#node_name GoogleMigrationCenterPreferenceSet#node_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47091ffd2aae97e4b90a55531c05ba89f09a291e343ef89490b5ddad8fdeede1)
            check_type(argname="argument node_name", value=node_name, expected_type=type_hints["node_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_name is not None:
            self._values["node_name"] = node_name

    @builtins.property
    def node_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Sole Tenant node. Consult https://cloud.google.com/compute/docs/nodes/sole-tenant-nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#node_name GoogleMigrationCenterPreferenceSet#node_name}
        '''
        result = self._values.get("node_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ada60249c8ff69a7bdfc582cdd91d08043bba0a43309b906406043c787185473)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d56766895e481182783edefa52027f5990fa0a7052d60356c3dc76ef8ba3a58)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99c4f9f956b1d1f9b2f99b07d9ed2c73a791b240d98f6d15b41c4c7f574b2ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ba804fd64982ab1e1dfdc50398363e18d7ed63b0516cf0c6a411b81c0582858)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88f188f6144c636815ca9ec32fd5d4f5f1448fdc290814d671ff67d34bf5bb9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f46a184f524e32674d5ce5c90c1a11f606e62352aafd951c03083a185d08624f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29500243af69804bc543be8df32cc756d84c4198de4cf1dc947af92eaf7403eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e1ebc84a25ba0c7b158bdb86f9e4718f9e22994dc98c6a679777e46ed7d10df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9adc621c932bdd1510a036fdffe461d8e437d77197a6f390c1ee4d90e64fe64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2171930b7f1e118d626d009d0282be30d546e84ef3df66c4eddf5d5d09c0a55a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeTypes")
    def put_node_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab914c9ca3cbe60af50cbdb0acb0ef2219e8ccad28f026b9dadda7f964d1db14)
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
    ) -> GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesList:
        return typing.cast(GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesList, jsii.get(self, "nodeTypes"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]], jsii.get(self, "nodeTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="commitmentPlan")
    def commitment_plan(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitmentPlan"))

    @commitment_plan.setter
    def commitment_plan(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb2f35aa44779e8c4e14ac0517dc92a0136b5ebbd107855dd136853e6d1e280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitmentPlan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuOvercommitRatio")
    def cpu_overcommit_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuOvercommitRatio"))

    @cpu_overcommit_ratio.setter
    def cpu_overcommit_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bcea3ca4ade099071423034702b4f51d9c83290a7d0234fca58fd932c490178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuOvercommitRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostMaintenancePolicy")
    def host_maintenance_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostMaintenancePolicy"))

    @host_maintenance_policy.setter
    def host_maintenance_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3130c2eb5f8ecde40acac18fd8117cb0d1c34a53148d2082fd12963b0ee1027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostMaintenancePolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences]:
        return typing.cast(typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14588190898fd002db8751fe6685ba03dd47e4ce4db509834fc9b34ff801354f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences",
    jsii_struct_bases=[],
    name_mapping={
        "commitment_plan": "commitmentPlan",
        "cpu_overcommit_ratio": "cpuOvercommitRatio",
        "memory_overcommit_ratio": "memoryOvercommitRatio",
        "storage_deduplication_compression_ratio": "storageDeduplicationCompressionRatio",
    },
)
class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences:
    def __init__(
        self,
        *,
        commitment_plan: typing.Optional[builtins.str] = None,
        cpu_overcommit_ratio: typing.Optional[jsii.Number] = None,
        memory_overcommit_ratio: typing.Optional[jsii.Number] = None,
        storage_deduplication_compression_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param commitment_plan: Commitment plan to consider when calculating costs for virtual machine insights and recommendations. If you are unsure which value to set, a 3 year commitment plan is often a good value to start with. Possible values: 'COMMITMENT_PLAN_UNSPECIFIED', 'ON_DEMAND', 'COMMITMENT_1_YEAR_MONTHLY_PAYMENTS', 'COMMITMENT_3_YEAR_MONTHLY_PAYMENTS', 'COMMITMENT_1_YEAR_UPFRONT_PAYMENT', 'COMMITMENT_3_YEAR_UPFRONT_PAYMENT', Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#commitment_plan GoogleMigrationCenterPreferenceSet#commitment_plan}
        :param cpu_overcommit_ratio: CPU overcommit ratio. Acceptable values are between 1.0 and 8.0, with 0.1 increment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#cpu_overcommit_ratio GoogleMigrationCenterPreferenceSet#cpu_overcommit_ratio}
        :param memory_overcommit_ratio: Memory overcommit ratio. Acceptable values are 1.0, 1.25, 1.5, 1.75 and 2.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#memory_overcommit_ratio GoogleMigrationCenterPreferenceSet#memory_overcommit_ratio}
        :param storage_deduplication_compression_ratio: The Deduplication and Compression ratio is based on the logical (Used Before) space required to store data before applying deduplication and compression, in relation to the physical (Used After) space required after applying deduplication and compression. Specifically, the ratio is the Used Before space divided by the Used After space. For example, if the Used Before space is 3 GB, but the physical Used After space is 1 GB, the deduplication and compression ratio is 3x. Acceptable values are between 1.0 and 4.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#storage_deduplication_compression_ratio GoogleMigrationCenterPreferenceSet#storage_deduplication_compression_ratio}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d017fbe861065d02e72f5bcbe4845be454ad737f4790c4e592cb44360071a85f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#commitment_plan GoogleMigrationCenterPreferenceSet#commitment_plan}
        '''
        result = self._values.get("commitment_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_overcommit_ratio(self) -> typing.Optional[jsii.Number]:
        '''CPU overcommit ratio. Acceptable values are between 1.0 and 8.0, with 0.1 increment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#cpu_overcommit_ratio GoogleMigrationCenterPreferenceSet#cpu_overcommit_ratio}
        '''
        result = self._values.get("cpu_overcommit_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_overcommit_ratio(self) -> typing.Optional[jsii.Number]:
        '''Memory overcommit ratio. Acceptable values are 1.0, 1.25, 1.5, 1.75 and 2.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#memory_overcommit_ratio GoogleMigrationCenterPreferenceSet#memory_overcommit_ratio}
        '''
        result = self._values.get("memory_overcommit_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_deduplication_compression_ratio(self) -> typing.Optional[jsii.Number]:
        '''The Deduplication and Compression ratio is based on the logical (Used Before) space required to store data before applying deduplication and compression, in relation to the physical (Used After) space required after applying deduplication and compression.

        Specifically, the ratio is the Used Before space divided by the Used After space. For example, if the Used Before space is 3 GB, but the physical Used After space is 1 GB, the deduplication and compression ratio is 3x. Acceptable values are between 1.0 and 4.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_migration_center_preference_set#storage_deduplication_compression_ratio GoogleMigrationCenterPreferenceSet#storage_deduplication_compression_ratio}
        '''
        result = self._values.get("storage_deduplication_compression_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMigrationCenterPreferenceSet.GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e2c2ab12ce0d72d670dd6d3471ebfd47a289089df8b430bb0b5ed64ce34554c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3915f69886ec7c7de16bd83b2b0fff7a886ac5570afd1ce9efcada23b7c78eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitmentPlan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuOvercommitRatio")
    def cpu_overcommit_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuOvercommitRatio"))

    @cpu_overcommit_ratio.setter
    def cpu_overcommit_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06343866a8a666896deb95efa175e39a074f9c3be8bdd3f3f9cf7b4cdd73f975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuOvercommitRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryOvercommitRatio")
    def memory_overcommit_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryOvercommitRatio"))

    @memory_overcommit_ratio.setter
    def memory_overcommit_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b82c470e22e88830175577e9d52af5d4bf4f44faa1efd4b75c6898ba5374d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryOvercommitRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageDeduplicationCompressionRatio")
    def storage_deduplication_compression_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageDeduplicationCompressionRatio"))

    @storage_deduplication_compression_ratio.setter
    def storage_deduplication_compression_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac28eec495e3034fc0dad2e726ad3a5fc1d682e16c450244fc685260d609b910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageDeduplicationCompressionRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences]:
        return typing.cast(typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18069dc5dd7f967685790de8e3c90eaea69c702186a7238eaf0dd4b184d6bf8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleMigrationCenterPreferenceSet",
    "GoogleMigrationCenterPreferenceSetConfig",
    "GoogleMigrationCenterPreferenceSetTimeouts",
    "GoogleMigrationCenterPreferenceSetTimeoutsOutputReference",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferences",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesList",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeriesOutputReference",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesOutputReference",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesOutputReference",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesOutputReference",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferencesOutputReference",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesList",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypesOutputReference",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesOutputReference",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences",
    "GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferencesOutputReference",
]

publication.publish()

def _typecheckingstub__38fe156dc34a01aba4cb2e32de7788746738d0c55835cdef438d5cb9dce84397(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    preference_set_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleMigrationCenterPreferenceSetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine_preferences: typing.Optional[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferences, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b8920ab546e3f688af88335825811b6426bd9debc453e48356f41f483de43846(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467ffb7752f95c0f6a1ca1a87368576403edf9e9d56250d81becb6aa410648fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d31200871f5bcbb432e5b1de8f19250d62e3fbd855aca4ad73c34948d0eb71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078f7008787769fe51ca2d90b019fee75e08e4e9eed5cb8afc88c6b9e33bfe22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776b1c017f9c92ed67b6564b4149a40ba01a997e10876a36fec9852cd0736630(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808ec2c4a7e049b5f4b61c2e4ac1e5e46d4ef4989831f32519656b3fa816af6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7241958697e27d50dcdf817f0f9a61f2647bfb2282c7388146a7dddfc4b12df1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c87d512ef836b9eeac03fc146891ae97922be320bad4ee7e13869efe54ca25(
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
    timeouts: typing.Optional[typing.Union[GoogleMigrationCenterPreferenceSetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine_preferences: typing.Optional[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferences, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8339eb1110abfafa8d871ef6d453f37ff8e1647ce2eaafc2d602f49a1b7c4be9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f018a03538f683b2f4331a5e60a1c1ecc3a22703185cae9a38e763e52c74374(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2099be04d97870fcaf843b2434147458e760f8359200d630eaa0926e2dbb955(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ee5ccf811e44e016e76a99dea044f252ebd1032d62a3f6364e717f4c198460(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c36ef6993f9be5372c3280bb2e7056de272ba11532dede78ff72075878c263(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf32b6cea28acd90b080be130b07ce6149a36edfd1eaca8c72d1bfa9e7a5345(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMigrationCenterPreferenceSetTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c1946ac0d17ac03ab38029e111f4a9a4d3da98ee6af26b90c8160e2f87a4bf(
    *,
    commitment_plan: typing.Optional[builtins.str] = None,
    compute_engine_preferences: typing.Optional[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    region_preferences: typing.Optional[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    sizing_optimization_strategy: typing.Optional[builtins.str] = None,
    sole_tenancy_preferences: typing.Optional[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    target_product: typing.Optional[builtins.str] = None,
    vmware_engine_preferences: typing.Optional[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79c7d90f2188df5b7160679d5997d8cb6d7e1a7ebe0e47a15b8bc597221ef35(
    *,
    license_type: typing.Optional[builtins.str] = None,
    machine_preferences: typing.Optional[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ea3a5e20e1f881bdc452e61c62303e2af805effcd931ed65fa40eb0f536c7f(
    *,
    allowed_machine_series: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d21d9dff74f23b97bb7f94e294f5cab555f0b23463cc5843502001240842ed(
    *,
    code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec6fb6b76b66571683d441533f11352d6cc10960208a9feabdef26257b36cf1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e542cbd94528e01e64c87fd0ccf95891340a2602f1b1bd67f78116962e8bdd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f353168a2dda1096a1dfde6abe0275145b61e356529a9b607a3d1f4467df00a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ed5ba008dcae85874b0b69f1856ab255473fd67a57a128c7f93d9df5f3ff4f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3342eb9fc3da3482e6a14bac253030f1d95993e31e963ebf9d4118e1d5a5b282(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d72ae686bbf17940d1fcbbebe047aa6ddc751f9e0fdd6704cf3e0c8f1fa5b72(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea012cb694343af7edc4856f5d8832b9300b74aba6f1d1f95e9e50fd9bc5131(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947b62e94650555f1810eab361e653a2a2d0b409247b94f75721c2cd966533b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442a2265786688e7d9953c772911c3dadcc473a369d9a525af50dad0a24676bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54de2a7ce012d0f37710e89b87d1dfffe710818cd5c624bbd9eb18dd03fc4d8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb7db1bafe9d13112d441b81b40fd511a7a4dd61595603b8371e666d449053b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferencesAllowedMachineSeries, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd95e222530a82940e9f95c8d1b145a32ea909005dded010dd25b08d22dcecb3(
    value: typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferencesMachinePreferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96d60a7da74070bf67c572d448305cb17714136779ddb3721c1520b1c806c76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa97ac32367cbb60bab480e9a9a5ff4cf652dbabb46ced3390d9b606cda39227(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df787470074e8f94dac2d571c84f383b49160df5b2dcffe2b4689de806ddad06(
    value: typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesComputeEnginePreferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e5ff7988c86491ded9c4837efa923ebea686e5b0761c465e2e4cbc822c95ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc8cf0df83de018484b193e9cec318b2de305b597c3bc6c6b6fdb1cd1cea7b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654fec476729e887207499224ca1ebf978ab6321904951f5774d5011d22c9d58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f56cfa109a69e2062dd97cc79ac3bde934d1126d5350dd744c39c517edfd36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__658782bc3cba5fa95dd561770b9dde3832d1f16e24ede90cefe46805ae2c6f9a(
    value: typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd85b9016875e03ab8dbdba30e86b23442d367d79689e9ddc2327f5f5615f412(
    *,
    preferred_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714572eb257f0791d7c225bf9dfc20cc2aeb062ac1239e05712d275445a420fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79f5ded86b746749a895dca8da32f0ab14ac7e980e86ef4b629a8f43af40011(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e881972931596f304d618d62da95d89b5e92dca5dd6e1e9a2f992ef6ad6c94(
    value: typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesRegionPreferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14c38769da22c8dee6f16aa929b50dbf1d917fc3ac066fd6a9425218279f983(
    *,
    commitment_plan: typing.Optional[builtins.str] = None,
    cpu_overcommit_ratio: typing.Optional[jsii.Number] = None,
    host_maintenance_policy: typing.Optional[builtins.str] = None,
    node_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47091ffd2aae97e4b90a55531c05ba89f09a291e343ef89490b5ddad8fdeede1(
    *,
    node_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada60249c8ff69a7bdfc582cdd91d08043bba0a43309b906406043c787185473(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d56766895e481182783edefa52027f5990fa0a7052d60356c3dc76ef8ba3a58(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99c4f9f956b1d1f9b2f99b07d9ed2c73a791b240d98f6d15b41c4c7f574b2ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba804fd64982ab1e1dfdc50398363e18d7ed63b0516cf0c6a411b81c0582858(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f188f6144c636815ca9ec32fd5d4f5f1448fdc290814d671ff67d34bf5bb9d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f46a184f524e32674d5ce5c90c1a11f606e62352aafd951c03083a185d08624f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29500243af69804bc543be8df32cc756d84c4198de4cf1dc947af92eaf7403eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1ebc84a25ba0c7b158bdb86f9e4718f9e22994dc98c6a679777e46ed7d10df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9adc621c932bdd1510a036fdffe461d8e437d77197a6f390c1ee4d90e64fe64(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2171930b7f1e118d626d009d0282be30d546e84ef3df66c4eddf5d5d09c0a55a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab914c9ca3cbe60af50cbdb0acb0ef2219e8ccad28f026b9dadda7f964d1db14(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferencesNodeTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb2f35aa44779e8c4e14ac0517dc92a0136b5ebbd107855dd136853e6d1e280(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bcea3ca4ade099071423034702b4f51d9c83290a7d0234fca58fd932c490178(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3130c2eb5f8ecde40acac18fd8117cb0d1c34a53148d2082fd12963b0ee1027(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14588190898fd002db8751fe6685ba03dd47e4ce4db509834fc9b34ff801354f(
    value: typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesSoleTenancyPreferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d017fbe861065d02e72f5bcbe4845be454ad737f4790c4e592cb44360071a85f(
    *,
    commitment_plan: typing.Optional[builtins.str] = None,
    cpu_overcommit_ratio: typing.Optional[jsii.Number] = None,
    memory_overcommit_ratio: typing.Optional[jsii.Number] = None,
    storage_deduplication_compression_ratio: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2c2ab12ce0d72d670dd6d3471ebfd47a289089df8b430bb0b5ed64ce34554c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3915f69886ec7c7de16bd83b2b0fff7a886ac5570afd1ce9efcada23b7c78eae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06343866a8a666896deb95efa175e39a074f9c3be8bdd3f3f9cf7b4cdd73f975(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b82c470e22e88830175577e9d52af5d4bf4f44faa1efd4b75c6898ba5374d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac28eec495e3034fc0dad2e726ad3a5fc1d682e16c450244fc685260d609b910(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18069dc5dd7f967685790de8e3c90eaea69c702186a7238eaf0dd4b184d6bf8e(
    value: typing.Optional[GoogleMigrationCenterPreferenceSetVirtualMachinePreferencesVmwareEnginePreferences],
) -> None:
    """Type checking stubs"""
    pass
