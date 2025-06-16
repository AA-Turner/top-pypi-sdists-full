r'''
# `google_os_config_guest_policies`

Refer to the Terraform Registry for docs: [`google_os_config_guest_policies`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies).
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


class GoogleOsConfigGuestPolicies(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPolicies",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies google_os_config_guest_policies}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        assignment: typing.Union["GoogleOsConfigGuestPoliciesAssignment", typing.Dict[builtins.str, typing.Any]],
        guest_policy_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        etag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        package_repositories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesPackageRepositories", typing.Dict[builtins.str, typing.Any]]]]] = None,
        packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesPackages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        recipes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesRecipes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies google_os_config_guest_policies} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param assignment: assignment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#assignment GoogleOsConfigGuestPolicies#assignment}
        :param guest_policy_id: The logical name of the guest policy in the project with the following restrictions: * Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#guest_policy_id GoogleOsConfigGuestPolicies#guest_policy_id}
        :param description: Description of the guest policy. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#description GoogleOsConfigGuestPolicies#description}
        :param etag: The etag for this guest policy. If this is provided on update, it must match the server's etag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#etag GoogleOsConfigGuestPolicies#etag}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#id GoogleOsConfigGuestPolicies#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param package_repositories: package_repositories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#package_repositories GoogleOsConfigGuestPolicies#package_repositories}
        :param packages: packages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#packages GoogleOsConfigGuestPolicies#packages}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#project GoogleOsConfigGuestPolicies#project}.
        :param recipes: recipes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#recipes GoogleOsConfigGuestPolicies#recipes}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#timeouts GoogleOsConfigGuestPolicies#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddba10db3e7f3246eac1da9216e7ca0ea76cbaa1cbd2b06f5e72fc5fa32a212c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleOsConfigGuestPoliciesConfig(
            assignment=assignment,
            guest_policy_id=guest_policy_id,
            description=description,
            etag=etag,
            id=id,
            package_repositories=package_repositories,
            packages=packages,
            project=project,
            recipes=recipes,
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
        '''Generates CDKTF code for importing a GoogleOsConfigGuestPolicies resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleOsConfigGuestPolicies to import.
        :param import_from_id: The id of the existing GoogleOsConfigGuestPolicies that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleOsConfigGuestPolicies to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954c042769b419ec7e7785f15cfe4513494fc629169eede7e39240ef20d42b69)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAssignment")
    def put_assignment(
        self,
        *,
        group_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesAssignmentGroupLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesAssignmentOsTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param group_labels: group_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#group_labels GoogleOsConfigGuestPolicies#group_labels}
        :param instance_name_prefixes: Targets VM instances whose name starts with one of these prefixes. Like labels, this is another way to group VM instances when targeting configs, for example prefix="prod-". Only supported for project-level policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#instance_name_prefixes GoogleOsConfigGuestPolicies#instance_name_prefixes}
        :param instances: Targets any of the instances specified. Instances are specified by their URI in the form zones/[ZONE]/instances/[INSTANCE_NAME]. Instance targeting is uncommon and is supported to facilitate the management of changes by the instance or to target specific VM instances for development and testing. Only supported for project-level policies and must reference instances within this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#instances GoogleOsConfigGuestPolicies#instances}
        :param os_types: os_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#os_types GoogleOsConfigGuestPolicies#os_types}
        :param zones: Targets instances in any of these zones. Leave empty to target instances in any zone. Zonal targeting is uncommon and is supported to facilitate the management of changes by zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#zones GoogleOsConfigGuestPolicies#zones}
        '''
        value = GoogleOsConfigGuestPoliciesAssignment(
            group_labels=group_labels,
            instance_name_prefixes=instance_name_prefixes,
            instances=instances,
            os_types=os_types,
            zones=zones,
        )

        return typing.cast(None, jsii.invoke(self, "putAssignment", [value]))

    @jsii.member(jsii_name="putPackageRepositories")
    def put_package_repositories(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesPackageRepositories", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__563735b7ed55992676c1ee272fbd631d1f1624df957ec761523bcc724ff0f5cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPackageRepositories", [value]))

    @jsii.member(jsii_name="putPackages")
    def put_packages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesPackages", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363115a911ee9b470fcb3191c9c61b4d65a4eb7ddbf31f7fa8310429ec8bfbc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPackages", [value]))

    @jsii.member(jsii_name="putRecipes")
    def put_recipes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesRecipes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18286af7165ef3398d0dea8d5d2764cd328041b2fec44f0419432495ba8855be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRecipes", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#create GoogleOsConfigGuestPolicies#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#delete GoogleOsConfigGuestPolicies#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#update GoogleOsConfigGuestPolicies#update}.
        '''
        value = GoogleOsConfigGuestPoliciesTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEtag")
    def reset_etag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEtag", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPackageRepositories")
    def reset_package_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackageRepositories", []))

    @jsii.member(jsii_name="resetPackages")
    def reset_packages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackages", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRecipes")
    def reset_recipes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecipes", []))

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
    @jsii.member(jsii_name="assignment")
    def assignment(self) -> "GoogleOsConfigGuestPoliciesAssignmentOutputReference":
        return typing.cast("GoogleOsConfigGuestPoliciesAssignmentOutputReference", jsii.get(self, "assignment"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="packageRepositories")
    def package_repositories(
        self,
    ) -> "GoogleOsConfigGuestPoliciesPackageRepositoriesList":
        return typing.cast("GoogleOsConfigGuestPoliciesPackageRepositoriesList", jsii.get(self, "packageRepositories"))

    @builtins.property
    @jsii.member(jsii_name="packages")
    def packages(self) -> "GoogleOsConfigGuestPoliciesPackagesList":
        return typing.cast("GoogleOsConfigGuestPoliciesPackagesList", jsii.get(self, "packages"))

    @builtins.property
    @jsii.member(jsii_name="recipes")
    def recipes(self) -> "GoogleOsConfigGuestPoliciesRecipesList":
        return typing.cast("GoogleOsConfigGuestPoliciesRecipesList", jsii.get(self, "recipes"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleOsConfigGuestPoliciesTimeoutsOutputReference":
        return typing.cast("GoogleOsConfigGuestPoliciesTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="assignmentInput")
    def assignment_input(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesAssignment"]:
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesAssignment"], jsii.get(self, "assignmentInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="etagInput")
    def etag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "etagInput"))

    @builtins.property
    @jsii.member(jsii_name="guestPolicyIdInput")
    def guest_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "guestPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="packageRepositoriesInput")
    def package_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesPackageRepositories"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesPackageRepositories"]]], jsii.get(self, "packageRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="packagesInput")
    def packages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesPackages"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesPackages"]]], jsii.get(self, "packagesInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="recipesInput")
    def recipes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesRecipes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesRecipes"]]], jsii.get(self, "recipesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOsConfigGuestPoliciesTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOsConfigGuestPoliciesTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11fccfec326a6152512a4ba29491aef13e9843f8667369fc5ad08ad2e6180e27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @etag.setter
    def etag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa0a9e002112132bfb849833582cdc25663930412c15f4b2ad2475f1cbead3dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "etag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guestPolicyId")
    def guest_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guestPolicyId"))

    @guest_policy_id.setter
    def guest_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e74439cc330239de01c61b2b75efad746b1dfd4fc2037e1c98d42490106ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a586de588b29177e75d543de67f4e96f351fdcc8c3055691d9f24fc6c8aa75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f00a00f2ca16db4407a9cca702b84db403e02ae872bd661f1f66da9607cdef9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesAssignment",
    jsii_struct_bases=[],
    name_mapping={
        "group_labels": "groupLabels",
        "instance_name_prefixes": "instanceNamePrefixes",
        "instances": "instances",
        "os_types": "osTypes",
        "zones": "zones",
    },
)
class GoogleOsConfigGuestPoliciesAssignment:
    def __init__(
        self,
        *,
        group_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesAssignmentGroupLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesAssignmentOsTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param group_labels: group_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#group_labels GoogleOsConfigGuestPolicies#group_labels}
        :param instance_name_prefixes: Targets VM instances whose name starts with one of these prefixes. Like labels, this is another way to group VM instances when targeting configs, for example prefix="prod-". Only supported for project-level policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#instance_name_prefixes GoogleOsConfigGuestPolicies#instance_name_prefixes}
        :param instances: Targets any of the instances specified. Instances are specified by their URI in the form zones/[ZONE]/instances/[INSTANCE_NAME]. Instance targeting is uncommon and is supported to facilitate the management of changes by the instance or to target specific VM instances for development and testing. Only supported for project-level policies and must reference instances within this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#instances GoogleOsConfigGuestPolicies#instances}
        :param os_types: os_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#os_types GoogleOsConfigGuestPolicies#os_types}
        :param zones: Targets instances in any of these zones. Leave empty to target instances in any zone. Zonal targeting is uncommon and is supported to facilitate the management of changes by zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#zones GoogleOsConfigGuestPolicies#zones}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1f1985c3d6b021c0c3c3af8d4708cf37be1adf2d1a9619e02118c27621b3b1)
            check_type(argname="argument group_labels", value=group_labels, expected_type=type_hints["group_labels"])
            check_type(argname="argument instance_name_prefixes", value=instance_name_prefixes, expected_type=type_hints["instance_name_prefixes"])
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument os_types", value=os_types, expected_type=type_hints["os_types"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_labels is not None:
            self._values["group_labels"] = group_labels
        if instance_name_prefixes is not None:
            self._values["instance_name_prefixes"] = instance_name_prefixes
        if instances is not None:
            self._values["instances"] = instances
        if os_types is not None:
            self._values["os_types"] = os_types
        if zones is not None:
            self._values["zones"] = zones

    @builtins.property
    def group_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesAssignmentGroupLabels"]]]:
        '''group_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#group_labels GoogleOsConfigGuestPolicies#group_labels}
        '''
        result = self._values.get("group_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesAssignmentGroupLabels"]]], result)

    @builtins.property
    def instance_name_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Targets VM instances whose name starts with one of these prefixes.

        Like labels, this is another way to group VM instances when targeting configs,
        for example prefix="prod-".
        Only supported for project-level policies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#instance_name_prefixes GoogleOsConfigGuestPolicies#instance_name_prefixes}
        '''
        result = self._values.get("instance_name_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Targets any of the instances specified.

        Instances are specified by their URI in the form
        zones/[ZONE]/instances/[INSTANCE_NAME].
        Instance targeting is uncommon and is supported to facilitate the management of changes
        by the instance or to target specific VM instances for development and testing.
        Only supported for project-level policies and must reference instances within this project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#instances GoogleOsConfigGuestPolicies#instances}
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def os_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesAssignmentOsTypes"]]]:
        '''os_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#os_types GoogleOsConfigGuestPolicies#os_types}
        '''
        result = self._values.get("os_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesAssignmentOsTypes"]]], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Targets instances in any of these zones.

        Leave empty to target instances in any zone.
        Zonal targeting is uncommon and is supported to facilitate the management of changes by zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#zones GoogleOsConfigGuestPolicies#zones}
        '''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesAssignment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesAssignmentGroupLabels",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class GoogleOsConfigGuestPoliciesAssignmentGroupLabels:
    def __init__(self, *, labels: typing.Mapping[builtins.str, builtins.str]) -> None:
        '''
        :param labels: Google Compute Engine instance labels that must be present for an instance to be included in this assignment group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#labels GoogleOsConfigGuestPolicies#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce28a2a09ebf824c0ee3e5faf2a12611e2ffa18103853fc104d59c6be060ea6)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "labels": labels,
        }

    @builtins.property
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Google Compute Engine instance labels that must be present for an instance to be included in this assignment group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#labels GoogleOsConfigGuestPolicies#labels}
        '''
        result = self._values.get("labels")
        assert result is not None, "Required property 'labels' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesAssignmentGroupLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesAssignmentGroupLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesAssignmentGroupLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__390e75c03430f1c7b1742681fae8eab0b00701855462b985a46f46f0143d86f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigGuestPoliciesAssignmentGroupLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9d1186c9d685e0b972575d8f0802d94a35430521b36afb33c0baf82204b54c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigGuestPoliciesAssignmentGroupLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f98c33897a781f477494ce2b90b91a0de2bf3310695e8701a8a717c842bbad7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be1f99b1f1b87b91d830efd0fda61bf95f55a9a743dc6d2ff5994d38b4682834)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b744c49a89de0f6f3d23c9167c5d944947763c5036513b7d293654ebf78738f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesAssignmentGroupLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesAssignmentGroupLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesAssignmentGroupLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66afbe395bc7dbe552b92282e4c4d460b5bfba8502e2dc8fbea623ab8a803777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesAssignmentGroupLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesAssignmentGroupLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0105a2e159ddc2d2dadfaae3c06e142c5bc463a00a9e91f2d7c0bd4d418c6093)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c43f574170fed6a0ff5a307608222727ff0740a0ba71c8591dbb879cc59468f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesAssignmentGroupLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesAssignmentGroupLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesAssignmentGroupLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1c9103ee7b864a8bb0c09c25b001a9ed8b0068b7e1de9f66cbeae6d41397f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesAssignmentOsTypes",
    jsii_struct_bases=[],
    name_mapping={
        "os_architecture": "osArchitecture",
        "os_short_name": "osShortName",
        "os_version": "osVersion",
    },
)
class GoogleOsConfigGuestPoliciesAssignmentOsTypes:
    def __init__(
        self,
        *,
        os_architecture: typing.Optional[builtins.str] = None,
        os_short_name: typing.Optional[builtins.str] = None,
        os_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_architecture: Targets VM instances with OS Inventory enabled and having the following OS architecture. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#os_architecture GoogleOsConfigGuestPolicies#os_architecture}
        :param os_short_name: Targets VM instances with OS Inventory enabled and having the following OS short name, for example "debian" or "windows". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#os_short_name GoogleOsConfigGuestPolicies#os_short_name}
        :param os_version: Targets VM instances with OS Inventory enabled and having the following following OS version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#os_version GoogleOsConfigGuestPolicies#os_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdb9662bc74c188498f24081a32f554e54897c8b226303830b5d930fca991a2e)
            check_type(argname="argument os_architecture", value=os_architecture, expected_type=type_hints["os_architecture"])
            check_type(argname="argument os_short_name", value=os_short_name, expected_type=type_hints["os_short_name"])
            check_type(argname="argument os_version", value=os_version, expected_type=type_hints["os_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if os_architecture is not None:
            self._values["os_architecture"] = os_architecture
        if os_short_name is not None:
            self._values["os_short_name"] = os_short_name
        if os_version is not None:
            self._values["os_version"] = os_version

    @builtins.property
    def os_architecture(self) -> typing.Optional[builtins.str]:
        '''Targets VM instances with OS Inventory enabled and having the following OS architecture.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#os_architecture GoogleOsConfigGuestPolicies#os_architecture}
        '''
        result = self._values.get("os_architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_short_name(self) -> typing.Optional[builtins.str]:
        '''Targets VM instances with OS Inventory enabled and having the following OS short name, for example "debian" or "windows".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#os_short_name GoogleOsConfigGuestPolicies#os_short_name}
        '''
        result = self._values.get("os_short_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_version(self) -> typing.Optional[builtins.str]:
        '''Targets VM instances with OS Inventory enabled and having the following following OS version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#os_version GoogleOsConfigGuestPolicies#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesAssignmentOsTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesAssignmentOsTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesAssignmentOsTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c334f79ae949b60ee6a6bb1ce42d8187b15305827e2aba0ffb973e91dfc8b2d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigGuestPoliciesAssignmentOsTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8adce14fcdd6c370d3b43d9136b7e3bf182078608077b086ffe2b01680bf671)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigGuestPoliciesAssignmentOsTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b1d955ee3a93ad6f0b9cbf43d21e180acc67954aebe386ec46dcddf84f519ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db07ac8ca123c2795aef58e167b7fd6f57f3bb45240de542ea0b171cd3d56906)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c1903394f51a63a37cc113bc63eed221c49611e0828d5669180d5af4e582779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesAssignmentOsTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesAssignmentOsTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesAssignmentOsTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f33a72c6c4ef8bbbd5275ddbefc4a22095768671a1a6b65da417d7d0bf975189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesAssignmentOsTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesAssignmentOsTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bf13d5ec203c8cc8c0a32e28aa4d143162c54abdd8d9676c463181472bce6aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOsArchitecture")
    def reset_os_architecture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsArchitecture", []))

    @jsii.member(jsii_name="resetOsShortName")
    def reset_os_short_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsShortName", []))

    @jsii.member(jsii_name="resetOsVersion")
    def reset_os_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsVersion", []))

    @builtins.property
    @jsii.member(jsii_name="osArchitectureInput")
    def os_architecture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osArchitectureInput"))

    @builtins.property
    @jsii.member(jsii_name="osShortNameInput")
    def os_short_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osShortNameInput"))

    @builtins.property
    @jsii.member(jsii_name="osVersionInput")
    def os_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="osArchitecture")
    def os_architecture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osArchitecture"))

    @os_architecture.setter
    def os_architecture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14bb08c61f28ea9b2e743414936f79d196c23044be964c97bce005d49f122c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osArchitecture", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osShortName")
    def os_short_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osShortName"))

    @os_short_name.setter
    def os_short_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2677cfb6ee49f4c13cf2a3a0c1108e3b0c5e0742f03ede121c6f5da85d3b070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osShortName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43cb4570293e7379cce7f3d4037ba33928e242ce0cfd2ecff99ae0b04848959f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesAssignmentOsTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesAssignmentOsTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesAssignmentOsTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf7af63191723fbc77264416536d1f7d015a951bd3c4813d1345297f4a71454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesAssignmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesAssignmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3880cc7f9e1054ab170c2cc8d6708414ffabc44238aecd1d707c2548bef81f5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGroupLabels")
    def put_group_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesAssignmentGroupLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55eca8116cc4925b94559de1ba5897f884e85a044fef648103f18b5d7db884b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGroupLabels", [value]))

    @jsii.member(jsii_name="putOsTypes")
    def put_os_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesAssignmentOsTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8956833d44d486c3183d4f09cf1370150aaa636710e03b7df3fadc86622a1ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOsTypes", [value]))

    @jsii.member(jsii_name="resetGroupLabels")
    def reset_group_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupLabels", []))

    @jsii.member(jsii_name="resetInstanceNamePrefixes")
    def reset_instance_name_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceNamePrefixes", []))

    @jsii.member(jsii_name="resetInstances")
    def reset_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstances", []))

    @jsii.member(jsii_name="resetOsTypes")
    def reset_os_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsTypes", []))

    @jsii.member(jsii_name="resetZones")
    def reset_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZones", []))

    @builtins.property
    @jsii.member(jsii_name="groupLabels")
    def group_labels(self) -> GoogleOsConfigGuestPoliciesAssignmentGroupLabelsList:
        return typing.cast(GoogleOsConfigGuestPoliciesAssignmentGroupLabelsList, jsii.get(self, "groupLabels"))

    @builtins.property
    @jsii.member(jsii_name="osTypes")
    def os_types(self) -> GoogleOsConfigGuestPoliciesAssignmentOsTypesList:
        return typing.cast(GoogleOsConfigGuestPoliciesAssignmentOsTypesList, jsii.get(self, "osTypes"))

    @builtins.property
    @jsii.member(jsii_name="groupLabelsInput")
    def group_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesAssignmentGroupLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesAssignmentGroupLabels]]], jsii.get(self, "groupLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceNamePrefixesInput")
    def instance_name_prefixes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instanceNamePrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="instancesInput")
    def instances_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instancesInput"))

    @builtins.property
    @jsii.member(jsii_name="osTypesInput")
    def os_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesAssignmentOsTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesAssignmentOsTypes]]], jsii.get(self, "osTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceNamePrefixes")
    def instance_name_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceNamePrefixes"))

    @instance_name_prefixes.setter
    def instance_name_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a53e0862c28df666c7791d4605907065291b854f8ad4704929e73e5616861b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceNamePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instances"))

    @instances.setter
    def instances(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb2836348627a82eb743a42fda27ae5fc97a0c8a14b1994193dabc51fab9f39d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba38e7d2377cde5a930c34eb4a1d4b0720593225d1bbf2a580de5a5292bf0b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleOsConfigGuestPoliciesAssignment]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesAssignment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesAssignment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85e025ac358ea93d1b7da08c2c6a54783acb2ade441aa122e5b5a668a489382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "assignment": "assignment",
        "guest_policy_id": "guestPolicyId",
        "description": "description",
        "etag": "etag",
        "id": "id",
        "package_repositories": "packageRepositories",
        "packages": "packages",
        "project": "project",
        "recipes": "recipes",
        "timeouts": "timeouts",
    },
)
class GoogleOsConfigGuestPoliciesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        assignment: typing.Union[GoogleOsConfigGuestPoliciesAssignment, typing.Dict[builtins.str, typing.Any]],
        guest_policy_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        etag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        package_repositories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesPackageRepositories", typing.Dict[builtins.str, typing.Any]]]]] = None,
        packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesPackages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        recipes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesRecipes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param assignment: assignment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#assignment GoogleOsConfigGuestPolicies#assignment}
        :param guest_policy_id: The logical name of the guest policy in the project with the following restrictions: * Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#guest_policy_id GoogleOsConfigGuestPolicies#guest_policy_id}
        :param description: Description of the guest policy. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#description GoogleOsConfigGuestPolicies#description}
        :param etag: The etag for this guest policy. If this is provided on update, it must match the server's etag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#etag GoogleOsConfigGuestPolicies#etag}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#id GoogleOsConfigGuestPolicies#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param package_repositories: package_repositories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#package_repositories GoogleOsConfigGuestPolicies#package_repositories}
        :param packages: packages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#packages GoogleOsConfigGuestPolicies#packages}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#project GoogleOsConfigGuestPolicies#project}.
        :param recipes: recipes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#recipes GoogleOsConfigGuestPolicies#recipes}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#timeouts GoogleOsConfigGuestPolicies#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(assignment, dict):
            assignment = GoogleOsConfigGuestPoliciesAssignment(**assignment)
        if isinstance(timeouts, dict):
            timeouts = GoogleOsConfigGuestPoliciesTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24fce410ec029d89e7f4b2b42f6c1e6fedc785a033057c55df832041d71816de)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument assignment", value=assignment, expected_type=type_hints["assignment"])
            check_type(argname="argument guest_policy_id", value=guest_policy_id, expected_type=type_hints["guest_policy_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument package_repositories", value=package_repositories, expected_type=type_hints["package_repositories"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument recipes", value=recipes, expected_type=type_hints["recipes"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assignment": assignment,
            "guest_policy_id": guest_policy_id,
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
        if etag is not None:
            self._values["etag"] = etag
        if id is not None:
            self._values["id"] = id
        if package_repositories is not None:
            self._values["package_repositories"] = package_repositories
        if packages is not None:
            self._values["packages"] = packages
        if project is not None:
            self._values["project"] = project
        if recipes is not None:
            self._values["recipes"] = recipes
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
    def assignment(self) -> GoogleOsConfigGuestPoliciesAssignment:
        '''assignment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#assignment GoogleOsConfigGuestPolicies#assignment}
        '''
        result = self._values.get("assignment")
        assert result is not None, "Required property 'assignment' is missing"
        return typing.cast(GoogleOsConfigGuestPoliciesAssignment, result)

    @builtins.property
    def guest_policy_id(self) -> builtins.str:
        '''The logical name of the guest policy in the project with the following restrictions: * Must contain only lowercase letters, numbers, and hyphens.

        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#guest_policy_id GoogleOsConfigGuestPolicies#guest_policy_id}
        '''
        result = self._values.get("guest_policy_id")
        assert result is not None, "Required property 'guest_policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the guest policy. Length of the description is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#description GoogleOsConfigGuestPolicies#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def etag(self) -> typing.Optional[builtins.str]:
        '''The etag for this guest policy. If this is provided on update, it must match the server's etag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#etag GoogleOsConfigGuestPolicies#etag}
        '''
        result = self._values.get("etag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#id GoogleOsConfigGuestPolicies#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_repositories(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesPackageRepositories"]]]:
        '''package_repositories block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#package_repositories GoogleOsConfigGuestPolicies#package_repositories}
        '''
        result = self._values.get("package_repositories")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesPackageRepositories"]]], result)

    @builtins.property
    def packages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesPackages"]]]:
        '''packages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#packages GoogleOsConfigGuestPolicies#packages}
        '''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesPackages"]]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#project GoogleOsConfigGuestPolicies#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesRecipes"]]]:
        '''recipes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#recipes GoogleOsConfigGuestPolicies#recipes}
        '''
        result = self._values.get("recipes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesRecipes"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleOsConfigGuestPoliciesTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#timeouts GoogleOsConfigGuestPolicies#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackageRepositories",
    jsii_struct_bases=[],
    name_mapping={"apt": "apt", "goo": "goo", "yum": "yum", "zypper": "zypper"},
)
class GoogleOsConfigGuestPoliciesPackageRepositories:
    def __init__(
        self,
        *,
        apt: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesPackageRepositoriesApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesPackageRepositoriesGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesPackageRepositoriesYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesPackageRepositoriesZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#apt GoogleOsConfigGuestPolicies#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#goo GoogleOsConfigGuestPolicies#goo}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#yum GoogleOsConfigGuestPolicies#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#zypper GoogleOsConfigGuestPolicies#zypper}
        '''
        if isinstance(apt, dict):
            apt = GoogleOsConfigGuestPoliciesPackageRepositoriesApt(**apt)
        if isinstance(goo, dict):
            goo = GoogleOsConfigGuestPoliciesPackageRepositoriesGoo(**goo)
        if isinstance(yum, dict):
            yum = GoogleOsConfigGuestPoliciesPackageRepositoriesYum(**yum)
        if isinstance(zypper, dict):
            zypper = GoogleOsConfigGuestPoliciesPackageRepositoriesZypper(**zypper)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bcc07c6b4912d834e43d4241ec40a67716206c2327c8aacec034edc9c2b8c1c)
            check_type(argname="argument apt", value=apt, expected_type=type_hints["apt"])
            check_type(argname="argument goo", value=goo, expected_type=type_hints["goo"])
            check_type(argname="argument yum", value=yum, expected_type=type_hints["yum"])
            check_type(argname="argument zypper", value=zypper, expected_type=type_hints["zypper"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apt is not None:
            self._values["apt"] = apt
        if goo is not None:
            self._values["goo"] = goo
        if yum is not None:
            self._values["yum"] = yum
        if zypper is not None:
            self._values["zypper"] = zypper

    @builtins.property
    def apt(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesPackageRepositoriesApt"]:
        '''apt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#apt GoogleOsConfigGuestPolicies#apt}
        '''
        result = self._values.get("apt")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesPackageRepositoriesApt"], result)

    @builtins.property
    def goo(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesPackageRepositoriesGoo"]:
        '''goo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#goo GoogleOsConfigGuestPolicies#goo}
        '''
        result = self._values.get("goo")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesPackageRepositoriesGoo"], result)

    @builtins.property
    def yum(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesPackageRepositoriesYum"]:
        '''yum block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#yum GoogleOsConfigGuestPolicies#yum}
        '''
        result = self._values.get("yum")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesPackageRepositoriesYum"], result)

    @builtins.property
    def zypper(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesPackageRepositoriesZypper"]:
        '''zypper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#zypper GoogleOsConfigGuestPolicies#zypper}
        '''
        result = self._values.get("zypper")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesPackageRepositoriesZypper"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesPackageRepositories(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackageRepositoriesApt",
    jsii_struct_bases=[],
    name_mapping={
        "components": "components",
        "distribution": "distribution",
        "uri": "uri",
        "archive_type": "archiveType",
        "gpg_key": "gpgKey",
    },
)
class GoogleOsConfigGuestPoliciesPackageRepositoriesApt:
    def __init__(
        self,
        *,
        components: typing.Sequence[builtins.str],
        distribution: builtins.str,
        uri: builtins.str,
        archive_type: typing.Optional[builtins.str] = None,
        gpg_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param components: List of components for this repository. Must contain at least one item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#components GoogleOsConfigGuestPolicies#components}
        :param distribution: Distribution of this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#distribution GoogleOsConfigGuestPolicies#distribution}
        :param uri: URI for this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#uri GoogleOsConfigGuestPolicies#uri}
        :param archive_type: Type of archive files in this repository. The default behavior is DEB. Default value: "DEB" Possible values: ["DEB", "DEB_SRC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#archive_type GoogleOsConfigGuestPolicies#archive_type}
        :param gpg_key: URI of the key file for this repository. The agent maintains a keyring at /etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg containing all the keys in any applied guest policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#gpg_key GoogleOsConfigGuestPolicies#gpg_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__531629a71ac016afd4b841f4a2200725d78dbb4c71a5354071710945d91e4ad1)
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument archive_type", value=archive_type, expected_type=type_hints["archive_type"])
            check_type(argname="argument gpg_key", value=gpg_key, expected_type=type_hints["gpg_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "components": components,
            "distribution": distribution,
            "uri": uri,
        }
        if archive_type is not None:
            self._values["archive_type"] = archive_type
        if gpg_key is not None:
            self._values["gpg_key"] = gpg_key

    @builtins.property
    def components(self) -> typing.List[builtins.str]:
        '''List of components for this repository. Must contain at least one item.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#components GoogleOsConfigGuestPolicies#components}
        '''
        result = self._values.get("components")
        assert result is not None, "Required property 'components' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def distribution(self) -> builtins.str:
        '''Distribution of this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#distribution GoogleOsConfigGuestPolicies#distribution}
        '''
        result = self._values.get("distribution")
        assert result is not None, "Required property 'distribution' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI for this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#uri GoogleOsConfigGuestPolicies#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archive_type(self) -> typing.Optional[builtins.str]:
        '''Type of archive files in this repository. The default behavior is DEB. Default value: "DEB" Possible values: ["DEB", "DEB_SRC"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#archive_type GoogleOsConfigGuestPolicies#archive_type}
        '''
        result = self._values.get("archive_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpg_key(self) -> typing.Optional[builtins.str]:
        '''URI of the key file for this repository.

        The agent maintains a keyring at
        /etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg containing all the keys in any applied guest policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#gpg_key GoogleOsConfigGuestPolicies#gpg_key}
        '''
        result = self._values.get("gpg_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesPackageRepositoriesApt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesPackageRepositoriesAptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackageRepositoriesAptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e33ff132182b3833fcd84d52599e2d7ccc5656e3cebb9b5dbe047b627eea0a68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArchiveType")
    def reset_archive_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveType", []))

    @jsii.member(jsii_name="resetGpgKey")
    def reset_gpg_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpgKey", []))

    @builtins.property
    @jsii.member(jsii_name="archiveTypeInput")
    def archive_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "archiveTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="componentsInput")
    def components_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "componentsInput"))

    @builtins.property
    @jsii.member(jsii_name="distributionInput")
    def distribution_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distributionInput"))

    @builtins.property
    @jsii.member(jsii_name="gpgKeyInput")
    def gpg_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gpgKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveType")
    def archive_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "archiveType"))

    @archive_type.setter
    def archive_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86841b5fc083090f66fd3ea04548c54b4db67dcbbb49b0b7b73f6a9b453fb96d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "components"))

    @components.setter
    def components(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a543fc4d2fb380ec06ebc238d83b7d8422c0d8eb56822f89aad987c1a8a8d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distribution"))

    @distribution.setter
    def distribution(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b507f1ac3a7d9ced4a9c44e3f242d9e0ca135bf1a827744cca41c15e1da1448e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distribution", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKey")
    def gpg_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpgKey"))

    @gpg_key.setter
    def gpg_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f65d9e666a087c328463872dd3849b489fa9893d5436e1f7ef394bdec09f769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a67954630ae7ecd1a3b047b6eeff0ba208d38ef74ab2146051f60ae83cdfb65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesApt]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesApt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesApt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__427d5ba88d69f473327d29351dcb72d73a03df9dcbfa25a20806b0a9deb774e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackageRepositoriesGoo",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "url": "url"},
)
class GoogleOsConfigGuestPoliciesPackageRepositoriesGoo:
    def __init__(self, *, name: builtins.str, url: builtins.str) -> None:
        '''
        :param name: The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#name GoogleOsConfigGuestPolicies#name}
        :param url: The url of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#url GoogleOsConfigGuestPolicies#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3070d00cb5bcf5d8ef357d89c3010ef9c012292e58680a56ca5b44e8cdd5c699)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "url": url,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#name GoogleOsConfigGuestPolicies#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The url of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#url GoogleOsConfigGuestPolicies#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesPackageRepositoriesGoo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesPackageRepositoriesGooOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackageRepositoriesGooOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06f2dda48c3533337dc9db590bec756bd7c951903de4c95c70c6aefe53b855f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c404e4cdafec3bec20dd10f946a62a37c360092580bf6ddccf33943e6f0c535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74fdd1625db4b080f46b3bf1ca203e56d1817eb4bce71da2fc8a595844e96f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesGoo]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesGoo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesGoo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa82809b0bd950c7413e6e8dfc120836ce38af8d4deee11894bd94723d243e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesPackageRepositoriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackageRepositoriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fd9dc63fb0a252f5d06dd1b5250d5cac2111faf4dcd0e93406a508e7f3692d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigGuestPoliciesPackageRepositoriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92150ccf23a8e94ed20e39af886ff167c47b89a2031086281e775a3774ea40d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigGuestPoliciesPackageRepositoriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18f6bdd219fa8321787d26ec1025939509fa65ce45231124ed72fc2af99e38df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b8de0d5db8d58c2fabaaf342098f74a368ef94f6a96f15a0ff25f2673dfbc30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be9bc1d6c72d4ac39240cdbeb02e518b97ee45765265251e5136ba65b250a7dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesPackageRepositories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesPackageRepositories]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesPackageRepositories]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3b75256cc9d1b83079eef01017048c0e8f5bb3f7050cdc155b5c6630871f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesPackageRepositoriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackageRepositoriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5b5f70f5564376f635a944bfa1d063858cfcf44ba123203ce29d119a18c6ce8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putApt")
    def put_apt(
        self,
        *,
        components: typing.Sequence[builtins.str],
        distribution: builtins.str,
        uri: builtins.str,
        archive_type: typing.Optional[builtins.str] = None,
        gpg_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param components: List of components for this repository. Must contain at least one item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#components GoogleOsConfigGuestPolicies#components}
        :param distribution: Distribution of this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#distribution GoogleOsConfigGuestPolicies#distribution}
        :param uri: URI for this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#uri GoogleOsConfigGuestPolicies#uri}
        :param archive_type: Type of archive files in this repository. The default behavior is DEB. Default value: "DEB" Possible values: ["DEB", "DEB_SRC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#archive_type GoogleOsConfigGuestPolicies#archive_type}
        :param gpg_key: URI of the key file for this repository. The agent maintains a keyring at /etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg containing all the keys in any applied guest policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#gpg_key GoogleOsConfigGuestPolicies#gpg_key}
        '''
        value = GoogleOsConfigGuestPoliciesPackageRepositoriesApt(
            components=components,
            distribution=distribution,
            uri=uri,
            archive_type=archive_type,
            gpg_key=gpg_key,
        )

        return typing.cast(None, jsii.invoke(self, "putApt", [value]))

    @jsii.member(jsii_name="putGoo")
    def put_goo(self, *, name: builtins.str, url: builtins.str) -> None:
        '''
        :param name: The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#name GoogleOsConfigGuestPolicies#name}
        :param url: The url of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#url GoogleOsConfigGuestPolicies#url}
        '''
        value = GoogleOsConfigGuestPoliciesPackageRepositoriesGoo(name=name, url=url)

        return typing.cast(None, jsii.invoke(self, "putGoo", [value]))

    @jsii.member(jsii_name="putYum")
    def put_yum(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#base_url GoogleOsConfigGuestPolicies#base_url}
        :param id: A one word, unique name for this repository. This is the repo id in the Yum config file and also the displayName if displayName is omitted. This id is also used as the unique identifier when checking for guest policy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#id GoogleOsConfigGuestPolicies#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#display_name GoogleOsConfigGuestPolicies#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#gpg_keys GoogleOsConfigGuestPolicies#gpg_keys}
        '''
        value = GoogleOsConfigGuestPoliciesPackageRepositoriesYum(
            base_url=base_url, id=id, display_name=display_name, gpg_keys=gpg_keys
        )

        return typing.cast(None, jsii.invoke(self, "putYum", [value]))

    @jsii.member(jsii_name="putZypper")
    def put_zypper(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#base_url GoogleOsConfigGuestPolicies#base_url}
        :param id: A one word, unique name for this repository. This is the repo id in the zypper config file and also the displayName if displayName is omitted. This id is also used as the unique identifier when checking for guest policy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#id GoogleOsConfigGuestPolicies#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#display_name GoogleOsConfigGuestPolicies#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#gpg_keys GoogleOsConfigGuestPolicies#gpg_keys}
        '''
        value = GoogleOsConfigGuestPoliciesPackageRepositoriesZypper(
            base_url=base_url, id=id, display_name=display_name, gpg_keys=gpg_keys
        )

        return typing.cast(None, jsii.invoke(self, "putZypper", [value]))

    @jsii.member(jsii_name="resetApt")
    def reset_apt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApt", []))

    @jsii.member(jsii_name="resetGoo")
    def reset_goo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoo", []))

    @jsii.member(jsii_name="resetYum")
    def reset_yum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYum", []))

    @jsii.member(jsii_name="resetZypper")
    def reset_zypper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZypper", []))

    @builtins.property
    @jsii.member(jsii_name="apt")
    def apt(self) -> GoogleOsConfigGuestPoliciesPackageRepositoriesAptOutputReference:
        return typing.cast(GoogleOsConfigGuestPoliciesPackageRepositoriesAptOutputReference, jsii.get(self, "apt"))

    @builtins.property
    @jsii.member(jsii_name="goo")
    def goo(self) -> GoogleOsConfigGuestPoliciesPackageRepositoriesGooOutputReference:
        return typing.cast(GoogleOsConfigGuestPoliciesPackageRepositoriesGooOutputReference, jsii.get(self, "goo"))

    @builtins.property
    @jsii.member(jsii_name="yum")
    def yum(self) -> "GoogleOsConfigGuestPoliciesPackageRepositoriesYumOutputReference":
        return typing.cast("GoogleOsConfigGuestPoliciesPackageRepositoriesYumOutputReference", jsii.get(self, "yum"))

    @builtins.property
    @jsii.member(jsii_name="zypper")
    def zypper(
        self,
    ) -> "GoogleOsConfigGuestPoliciesPackageRepositoriesZypperOutputReference":
        return typing.cast("GoogleOsConfigGuestPoliciesPackageRepositoriesZypperOutputReference", jsii.get(self, "zypper"))

    @builtins.property
    @jsii.member(jsii_name="aptInput")
    def apt_input(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesApt]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesApt], jsii.get(self, "aptInput"))

    @builtins.property
    @jsii.member(jsii_name="gooInput")
    def goo_input(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesGoo]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesGoo], jsii.get(self, "gooInput"))

    @builtins.property
    @jsii.member(jsii_name="yumInput")
    def yum_input(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesPackageRepositoriesYum"]:
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesPackageRepositoriesYum"], jsii.get(self, "yumInput"))

    @builtins.property
    @jsii.member(jsii_name="zypperInput")
    def zypper_input(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesPackageRepositoriesZypper"]:
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesPackageRepositoriesZypper"], jsii.get(self, "zypperInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesPackageRepositories]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesPackageRepositories]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesPackageRepositories]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c498a4a8f089e29302dfe5e4d28a538bcbeb9711effa63dc2e5400373e69044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackageRepositoriesYum",
    jsii_struct_bases=[],
    name_mapping={
        "base_url": "baseUrl",
        "id": "id",
        "display_name": "displayName",
        "gpg_keys": "gpgKeys",
    },
)
class GoogleOsConfigGuestPoliciesPackageRepositoriesYum:
    def __init__(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#base_url GoogleOsConfigGuestPolicies#base_url}
        :param id: A one word, unique name for this repository. This is the repo id in the Yum config file and also the displayName if displayName is omitted. This id is also used as the unique identifier when checking for guest policy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#id GoogleOsConfigGuestPolicies#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#display_name GoogleOsConfigGuestPolicies#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#gpg_keys GoogleOsConfigGuestPolicies#gpg_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8690ef411d08e20c6d06c2312fa68a77a384f2f90f747eea0e1d43c33441a0)
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gpg_keys", value=gpg_keys, expected_type=type_hints["gpg_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_url": base_url,
            "id": id,
        }
        if display_name is not None:
            self._values["display_name"] = display_name
        if gpg_keys is not None:
            self._values["gpg_keys"] = gpg_keys

    @builtins.property
    def base_url(self) -> builtins.str:
        '''The location of the repository directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#base_url GoogleOsConfigGuestPolicies#base_url}
        '''
        result = self._values.get("base_url")
        assert result is not None, "Required property 'base_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''A one word, unique name for this repository.

        This is the repo id in the Yum config file and also the displayName
        if displayName is omitted. This id is also used as the unique identifier when checking for guest policy conflicts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#id GoogleOsConfigGuestPolicies#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#display_name GoogleOsConfigGuestPolicies#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URIs of GPG keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#gpg_keys GoogleOsConfigGuestPolicies#gpg_keys}
        '''
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesPackageRepositoriesYum(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesPackageRepositoriesYumOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackageRepositoriesYumOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62e3322934016b821c0c57ec32089f0121032576b50ad825747824f84887c7bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetGpgKeys")
    def reset_gpg_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpgKeys", []))

    @builtins.property
    @jsii.member(jsii_name="baseUrlInput")
    def base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gpgKeysInput")
    def gpg_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "gpgKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseUrl"))

    @base_url.setter
    def base_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9309461581e19e5effffa9843607eb2730accf75f70e5a9f92d217f76a730420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4ad93ec5f1801408222579e77ce871c29687e837fc902bbea0679db0847b50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKeys")
    def gpg_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gpgKeys"))

    @gpg_keys.setter
    def gpg_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39780b0e61762a0bc4339e08a4b2c528e96c0cc5371a9ba1476a09af0b081f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b34d2b4781f312f21931e4c3a6daff2fab3c647246a0857d9f44924a9c94ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesYum]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesYum], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesYum],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1589c5397c952998372d7ac09c4e208e631d474455527d8b842b2294e31de35d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackageRepositoriesZypper",
    jsii_struct_bases=[],
    name_mapping={
        "base_url": "baseUrl",
        "id": "id",
        "display_name": "displayName",
        "gpg_keys": "gpgKeys",
    },
)
class GoogleOsConfigGuestPoliciesPackageRepositoriesZypper:
    def __init__(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#base_url GoogleOsConfigGuestPolicies#base_url}
        :param id: A one word, unique name for this repository. This is the repo id in the zypper config file and also the displayName if displayName is omitted. This id is also used as the unique identifier when checking for guest policy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#id GoogleOsConfigGuestPolicies#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#display_name GoogleOsConfigGuestPolicies#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#gpg_keys GoogleOsConfigGuestPolicies#gpg_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb6e5d715d2a9fb500e7481e36da1affaa6bd76d1c6e3459f1e81826574a0933)
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gpg_keys", value=gpg_keys, expected_type=type_hints["gpg_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_url": base_url,
            "id": id,
        }
        if display_name is not None:
            self._values["display_name"] = display_name
        if gpg_keys is not None:
            self._values["gpg_keys"] = gpg_keys

    @builtins.property
    def base_url(self) -> builtins.str:
        '''The location of the repository directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#base_url GoogleOsConfigGuestPolicies#base_url}
        '''
        result = self._values.get("base_url")
        assert result is not None, "Required property 'base_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''A one word, unique name for this repository.

        This is the repo id in the zypper config file and also the displayName
        if displayName is omitted. This id is also used as the unique identifier when checking for guest policy conflicts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#id GoogleOsConfigGuestPolicies#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#display_name GoogleOsConfigGuestPolicies#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URIs of GPG keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#gpg_keys GoogleOsConfigGuestPolicies#gpg_keys}
        '''
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesPackageRepositoriesZypper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesPackageRepositoriesZypperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackageRepositoriesZypperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdfaa7b94f207df766a34156a264ac313d5a89a59ce0eace5626c2c10d86677c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetGpgKeys")
    def reset_gpg_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpgKeys", []))

    @builtins.property
    @jsii.member(jsii_name="baseUrlInput")
    def base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gpgKeysInput")
    def gpg_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "gpgKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseUrl"))

    @base_url.setter
    def base_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1a04d4158a82d0dd3d34ecbdb5f5773d0ed8dc6e5c0e4ae330380bd417e19d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e498bb806ec2d327e5ead9f60559b453b3c6458185b051c3f77c2b9a70e0db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKeys")
    def gpg_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gpgKeys"))

    @gpg_keys.setter
    def gpg_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__854e7acb35ac6ce85467f622b56d7e6083285fcfb5857a1526b889ad7b7ecaf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf6780af6ccca6dcd6a9e4c78efaded40082a60c6ffb3771131a0af9cf7d9cdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesZypper]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesZypper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesZypper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66272f314f1f0421174c5196b77759b35787137c4746ccb5864dddc141ed70b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackages",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "desired_state": "desiredState",
        "manager": "manager",
    },
)
class GoogleOsConfigGuestPoliciesPackages:
    def __init__(
        self,
        *,
        name: builtins.str,
        desired_state: typing.Optional[builtins.str] = None,
        manager: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the package. A package is uniquely identified for conflict validation by checking the package name and the manager(s) that the package targets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#name GoogleOsConfigGuestPolicies#name}
        :param desired_state: The desiredState the agent should maintain for this package. The default is to ensure the package is installed. Possible values: ["INSTALLED", "UPDATED", "REMOVED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#desired_state GoogleOsConfigGuestPolicies#desired_state}
        :param manager: Type of package manager that can be used to install this package. If a system does not have the package manager, the package is not installed or removed no error message is returned. By default, or if you specify ANY, the agent attempts to install and remove this package using the default package manager. This is useful when creating a policy that applies to different types of systems. The default behavior is ANY. Default value: "ANY" Possible values: ["ANY", "APT", "YUM", "ZYPPER", "GOO"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#manager GoogleOsConfigGuestPolicies#manager}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c1eabfc420c9e6b8c855e2a08cc88f82f34bbbd34594fb687b1ef79dff7f9a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
            check_type(argname="argument manager", value=manager, expected_type=type_hints["manager"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if desired_state is not None:
            self._values["desired_state"] = desired_state
        if manager is not None:
            self._values["manager"] = manager

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the package.

        A package is uniquely identified for conflict validation
        by checking the package name and the manager(s) that the package targets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#name GoogleOsConfigGuestPolicies#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def desired_state(self) -> typing.Optional[builtins.str]:
        '''The desiredState the agent should maintain for this package.

        The default is to ensure the package is installed. Possible values: ["INSTALLED", "UPDATED", "REMOVED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#desired_state GoogleOsConfigGuestPolicies#desired_state}
        '''
        result = self._values.get("desired_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manager(self) -> typing.Optional[builtins.str]:
        '''Type of package manager that can be used to install this package.

        If a system does not have the package manager,
        the package is not installed or removed no error message is returned. By default, or if you specify ANY,
        the agent attempts to install and remove this package using the default package manager.
        This is useful when creating a policy that applies to different types of systems.
        The default behavior is ANY. Default value: "ANY" Possible values: ["ANY", "APT", "YUM", "ZYPPER", "GOO"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#manager GoogleOsConfigGuestPolicies#manager}
        '''
        result = self._values.get("manager")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesPackages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesPackagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__904d9b08813cdc82227f50879e46b93341a0a2cbeb4fe4221e0e9740884d61f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigGuestPoliciesPackagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52585d5bcaafd546037ac566871217a031c07b7490b6af6580fb97509c6b32d9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigGuestPoliciesPackagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e5823903e9a99119e278973918433650ac646b88b3d035a9cdf4dced9661cfe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ca3dc7c677ff1fb0ccef675ddd5f0fbded3e018312eb77b0a491581618aa779)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b9fb14a3386e668f2a60490222a75cef9c7b5352ff535c4953c1a3476646a5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesPackages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesPackages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesPackages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c359e1746a9ebc644492fd36546927e9412ca39da7a8a55c9793d36719ee533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesPackagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesPackagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__891c314cd010230955cd6ef3991a1d1c743bc7904db2fd88f8f6c836afa59df6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDesiredState")
    def reset_desired_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredState", []))

    @jsii.member(jsii_name="resetManager")
    def reset_manager(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManager", []))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="managerInput")
    def manager_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managerInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3303efc10cf96cb596bee64d50447fc1dacf8636901d78f7ccf2099912811b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="manager")
    def manager(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manager"))

    @manager.setter
    def manager(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca0f3e0ada631a516a8f73cf6c2d048efe23ce6a304ec6f5878dfe85f61cfab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manager", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50f073495432a17d041294d3bb3912800c1ca544f566e7379db54b5c1e511ddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesPackages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesPackages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesPackages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a083ac1f8c8069e5e4b073ce05265c9083a5c12ddd9bab1d0c861faf02d7beb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "artifacts": "artifacts",
        "desired_state": "desiredState",
        "install_steps": "installSteps",
        "update_steps": "updateSteps",
        "version": "version",
    },
)
class GoogleOsConfigGuestPoliciesRecipes:
    def __init__(
        self,
        *,
        name: builtins.str,
        artifacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesRecipesArtifacts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        desired_state: typing.Optional[builtins.str] = None,
        install_steps: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesRecipesInstallSteps", typing.Dict[builtins.str, typing.Any]]]]] = None,
        update_steps: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesRecipesUpdateSteps", typing.Dict[builtins.str, typing.Any]]]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Unique identifier for the recipe. Only one recipe with a given name is installed on an instance. Names are also used to identify resources which helps to determine whether guest policies have conflicts. This means that requests to create multiple recipes with the same name and version are rejected since they could potentially have conflicting assignments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#name GoogleOsConfigGuestPolicies#name}
        :param artifacts: artifacts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifacts GoogleOsConfigGuestPolicies#artifacts}
        :param desired_state: Default is INSTALLED. The desired state the agent should maintain for this recipe. INSTALLED: The software recipe is installed on the instance but won't be updated to new versions. INSTALLED_KEEP_UPDATED: The software recipe is installed on the instance. The recipe is updated to a higher version, if a higher version of the recipe is assigned to this instance. REMOVE: Remove is unsupported for software recipes and attempts to create or update a recipe to the REMOVE state is rejected. Default value: "INSTALLED" Possible values: ["INSTALLED", "UPDATED", "REMOVED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#desired_state GoogleOsConfigGuestPolicies#desired_state}
        :param install_steps: install_steps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#install_steps GoogleOsConfigGuestPolicies#install_steps}
        :param update_steps: update_steps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#update_steps GoogleOsConfigGuestPolicies#update_steps}
        :param version: The version of this software recipe. Version can be up to 4 period separated numbers (e.g. 12.34.56.78). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#version GoogleOsConfigGuestPolicies#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ebf98f6b27dd77119a0053775a1c1e724fa5b1e073fd94e75d85c0b4e7b9be3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
            check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
            check_type(argname="argument install_steps", value=install_steps, expected_type=type_hints["install_steps"])
            check_type(argname="argument update_steps", value=update_steps, expected_type=type_hints["update_steps"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if desired_state is not None:
            self._values["desired_state"] = desired_state
        if install_steps is not None:
            self._values["install_steps"] = install_steps
        if update_steps is not None:
            self._values["update_steps"] = update_steps
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''Unique identifier for the recipe.

        Only one recipe with a given name is installed on an instance.
        Names are also used to identify resources which helps to determine whether guest policies have conflicts.
        This means that requests to create multiple recipes with the same name and version are rejected since they
        could potentially have conflicting assignments.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#name GoogleOsConfigGuestPolicies#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def artifacts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesRecipesArtifacts"]]]:
        '''artifacts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifacts GoogleOsConfigGuestPolicies#artifacts}
        '''
        result = self._values.get("artifacts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesRecipesArtifacts"]]], result)

    @builtins.property
    def desired_state(self) -> typing.Optional[builtins.str]:
        '''Default is INSTALLED. The desired state the agent should maintain for this recipe.

        INSTALLED: The software recipe is installed on the instance but won't be updated to new versions.
        INSTALLED_KEEP_UPDATED: The software recipe is installed on the instance. The recipe is updated to a higher version,
        if a higher version of the recipe is assigned to this instance.
        REMOVE: Remove is unsupported for software recipes and attempts to create or update a recipe to the REMOVE state is rejected. Default value: "INSTALLED" Possible values: ["INSTALLED", "UPDATED", "REMOVED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#desired_state GoogleOsConfigGuestPolicies#desired_state}
        '''
        result = self._values.get("desired_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_steps(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesRecipesInstallSteps"]]]:
        '''install_steps block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#install_steps GoogleOsConfigGuestPolicies#install_steps}
        '''
        result = self._values.get("install_steps")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesRecipesInstallSteps"]]], result)

    @builtins.property
    def update_steps(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesRecipesUpdateSteps"]]]:
        '''update_steps block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#update_steps GoogleOsConfigGuestPolicies#update_steps}
        '''
        result = self._values.get("update_steps")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesRecipesUpdateSteps"]]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The version of this software recipe. Version can be up to 4 period separated numbers (e.g. 12.34.56.78).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#version GoogleOsConfigGuestPolicies#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesArtifacts",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "remote": "remote",
    },
)
class GoogleOsConfigGuestPoliciesRecipesArtifacts:
    def __init__(
        self,
        *,
        id: builtins.str,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesArtifactsGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        remote: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesArtifactsRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Id of the artifact, which the installation and update steps of this recipe can reference. Artifacts in a recipe cannot have the same id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#id GoogleOsConfigGuestPolicies#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param allow_insecure: Defaults to false. When false, recipes are subject to validations based on the artifact type: Remote: A checksum must be specified, and only protocols with transport-layer security are permitted. GCS: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allow_insecure GoogleOsConfigGuestPolicies#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#gcs GoogleOsConfigGuestPolicies#gcs}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#remote GoogleOsConfigGuestPolicies#remote}
        '''
        if isinstance(gcs, dict):
            gcs = GoogleOsConfigGuestPoliciesRecipesArtifactsGcs(**gcs)
        if isinstance(remote, dict):
            remote = GoogleOsConfigGuestPoliciesRecipesArtifactsRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5837409d979e19082b61d3b36b18ad1e2235c619d4af05a7583c519250fc834d)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument allow_insecure", value=allow_insecure, expected_type=type_hints["allow_insecure"])
            check_type(argname="argument gcs", value=gcs, expected_type=type_hints["gcs"])
            check_type(argname="argument remote", value=remote, expected_type=type_hints["remote"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if allow_insecure is not None:
            self._values["allow_insecure"] = allow_insecure
        if gcs is not None:
            self._values["gcs"] = gcs
        if remote is not None:
            self._values["remote"] = remote

    @builtins.property
    def id(self) -> builtins.str:
        '''Id of the artifact, which the installation and update steps of this recipe can reference.

        Artifacts in a recipe cannot have the same id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#id GoogleOsConfigGuestPolicies#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defaults to false.

        When false, recipes are subject to validations based on the artifact type:
        Remote: A checksum must be specified, and only protocols with transport-layer security are permitted.
        GCS: An object generation number must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allow_insecure GoogleOsConfigGuestPolicies#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(self) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesArtifactsGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#gcs GoogleOsConfigGuestPolicies#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesArtifactsGcs"], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesArtifactsRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#remote GoogleOsConfigGuestPolicies#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesArtifactsRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesArtifacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesArtifactsGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "generation": "generation", "object": "object"},
)
class GoogleOsConfigGuestPoliciesRecipesArtifactsGcs:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        generation: typing.Optional[jsii.Number] = None,
        object: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Google Cloud Storage object. Given an example URL: https://storage.googleapis.com/my-bucket/foo/bar#1234567 this value would be my-bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#bucket GoogleOsConfigGuestPolicies#bucket}
        :param generation: Must be provided if allowInsecure is false. Generation number of the Google Cloud Storage object. https://storage.googleapis.com/my-bucket/foo/bar#1234567 this value would be 1234567. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#generation GoogleOsConfigGuestPolicies#generation}
        :param object: Name of the Google Cloud Storage object. Given an example URL: https://storage.googleapis.com/my-bucket/foo/bar#1234567 this value would be foo/bar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#object GoogleOsConfigGuestPolicies#object}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed4582fae3dd7d501b6927867166df6d8f4acb738a87d037e2bbcb38063f02a)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument generation", value=generation, expected_type=type_hints["generation"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if generation is not None:
            self._values["generation"] = generation
        if object is not None:
            self._values["object"] = object

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''Bucket of the Google Cloud Storage object. Given an example URL: https://storage.googleapis.com/my-bucket/foo/bar#1234567 this value would be my-bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#bucket GoogleOsConfigGuestPolicies#bucket}
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def generation(self) -> typing.Optional[jsii.Number]:
        '''Must be provided if allowInsecure is false.

        Generation number of the Google Cloud Storage object.
        https://storage.googleapis.com/my-bucket/foo/bar#1234567 this value would be 1234567.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#generation GoogleOsConfigGuestPolicies#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def object(self) -> typing.Optional[builtins.str]:
        '''Name of the Google Cloud Storage object. Given an example URL: https://storage.googleapis.com/my-bucket/foo/bar#1234567 this value would be foo/bar.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#object GoogleOsConfigGuestPolicies#object}
        '''
        result = self._values.get("object")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesArtifactsGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesArtifactsGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesArtifactsGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c37fec4105496c0d30b806fd74df267f36df421efcb2b4d6fdb409b2e2cdd85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetGeneration")
    def reset_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeneration", []))

    @jsii.member(jsii_name="resetObject")
    def reset_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObject", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="generationInput")
    def generation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "generationInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb8fc601e0c1e535c8dc603e94bd481f2f96f5dc49136a80072f29f441b4d67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ade151bf3cb2f386fefda775dbabd958f303c0981cd4bf7de0c3bb8e8d6bdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f04b6a429aa46072f749ecf6d3cfd342ae331304ba59a5768d31e20b9102d95e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesArtifactsGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesArtifactsGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesArtifactsGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ba1f254af275283f0776d56e607d0a67670db6d147231cf410d664d14919f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesRecipesArtifactsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesArtifactsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb837e4c28cc7899fbb788b46c4dc1815881cd87d2137f025c9808de312ff503)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigGuestPoliciesRecipesArtifactsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a79619db9841fdd78120a6608f48d44a989baa557589e7f45acc6be1eb8a59)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigGuestPoliciesRecipesArtifactsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2240311a16bcb4353afde828daa9cf1927a85a64f42d69b05b4e2657a36a5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73cdee26391d0b109d9aafa23cd28baf9826b78f2a3b8a90ba495c4aefb6b197)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b452068caad0dd94b1cf5273383ba2c4d5a8018680bd88a1f863d5aec615cde7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesArtifacts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesArtifacts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesArtifacts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d499d2c261dbdd500af4da94a42cc4dd2e1de078b9d0318eb16ac5613f2bf16e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesRecipesArtifactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesArtifactsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__182066da260adf61f38318ad731ce8b6cef56a1bc8a8881b33323c84cc5360ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        generation: typing.Optional[jsii.Number] = None,
        object: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Google Cloud Storage object. Given an example URL: https://storage.googleapis.com/my-bucket/foo/bar#1234567 this value would be my-bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#bucket GoogleOsConfigGuestPolicies#bucket}
        :param generation: Must be provided if allowInsecure is false. Generation number of the Google Cloud Storage object. https://storage.googleapis.com/my-bucket/foo/bar#1234567 this value would be 1234567. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#generation GoogleOsConfigGuestPolicies#generation}
        :param object: Name of the Google Cloud Storage object. Given an example URL: https://storage.googleapis.com/my-bucket/foo/bar#1234567 this value would be foo/bar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#object GoogleOsConfigGuestPolicies#object}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesArtifactsGcs(
            bucket=bucket, generation=generation, object=object
        )

        return typing.cast(None, jsii.invoke(self, "putGcs", [value]))

    @jsii.member(jsii_name="putRemote")
    def put_remote(
        self,
        *,
        check_sum: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param check_sum: Must be provided if allowInsecure is false. SHA256 checksum in hex format, to compare to the checksum of the artifact. If the checksum is not empty and it doesn't match the artifact then the recipe installation fails before running any of the steps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#check_sum GoogleOsConfigGuestPolicies#check_sum}
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format {protocol}://{location}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#uri GoogleOsConfigGuestPolicies#uri}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesArtifactsRemote(
            check_sum=check_sum, uri=uri
        )

        return typing.cast(None, jsii.invoke(self, "putRemote", [value]))

    @jsii.member(jsii_name="resetAllowInsecure")
    def reset_allow_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInsecure", []))

    @jsii.member(jsii_name="resetGcs")
    def reset_gcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcs", []))

    @jsii.member(jsii_name="resetRemote")
    def reset_remote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemote", []))

    @builtins.property
    @jsii.member(jsii_name="gcs")
    def gcs(self) -> GoogleOsConfigGuestPoliciesRecipesArtifactsGcsOutputReference:
        return typing.cast(GoogleOsConfigGuestPoliciesRecipesArtifactsGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "GoogleOsConfigGuestPoliciesRecipesArtifactsRemoteOutputReference":
        return typing.cast("GoogleOsConfigGuestPoliciesRecipesArtifactsRemoteOutputReference", jsii.get(self, "remote"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecureInput")
    def allow_insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInsecureInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsInput")
    def gcs_input(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesArtifactsGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesArtifactsGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesArtifactsRemote"]:
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesArtifactsRemote"], jsii.get(self, "remoteInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecure")
    def allow_insecure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowInsecure"))

    @allow_insecure.setter
    def allow_insecure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1252dfb29daa9a8e70bd2d864c2dd6227fbd5ed739947ef424c290b8c2123e98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b6b37dc985f03c6ec56c653c20aff4a06a5a3c441aab5fc3057b008e21b19c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipesArtifacts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipesArtifacts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipesArtifacts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb799e113e88decf4541b4241651b064a0de962e92a1ce6e94d1758494355406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesArtifactsRemote",
    jsii_struct_bases=[],
    name_mapping={"check_sum": "checkSum", "uri": "uri"},
)
class GoogleOsConfigGuestPoliciesRecipesArtifactsRemote:
    def __init__(
        self,
        *,
        check_sum: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param check_sum: Must be provided if allowInsecure is false. SHA256 checksum in hex format, to compare to the checksum of the artifact. If the checksum is not empty and it doesn't match the artifact then the recipe installation fails before running any of the steps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#check_sum GoogleOsConfigGuestPolicies#check_sum}
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format {protocol}://{location}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#uri GoogleOsConfigGuestPolicies#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c44ee9b9e65ef0f07af8d0d392c05b08bd3be49f803d7aaefa8bce3527ca0a)
            check_type(argname="argument check_sum", value=check_sum, expected_type=type_hints["check_sum"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if check_sum is not None:
            self._values["check_sum"] = check_sum
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def check_sum(self) -> typing.Optional[builtins.str]:
        '''Must be provided if allowInsecure is false.

        SHA256 checksum in hex format, to compare to the checksum of the artifact.
        If the checksum is not empty and it doesn't match the artifact then the recipe installation fails before running any
        of the steps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#check_sum GoogleOsConfigGuestPolicies#check_sum}
        '''
        result = self._values.get("check_sum")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''URI from which to fetch the object. It should contain both the protocol and path following the format {protocol}://{location}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#uri GoogleOsConfigGuestPolicies#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesArtifactsRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesArtifactsRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesArtifactsRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0547f6505ce7f409dc55cb95fdeabc86afb6de72ad216acc044ac4acf950fca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCheckSum")
    def reset_check_sum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckSum", []))

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="checkSumInput")
    def check_sum_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "checkSumInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="checkSum")
    def check_sum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "checkSum"))

    @check_sum.setter
    def check_sum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a075311f1b99469c09e5557a626afe46e8be9ccda8253db755647b801a1de20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkSum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d38be5b330d52a994b14f40ef627508c87f98e07f52c0fe61b4aacf68566ca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesArtifactsRemote]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesArtifactsRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesArtifactsRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f595e793df0c45a77dfeba93bcf69f76a9aac6f3d592e0f22b38536e0ca4191f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallSteps",
    jsii_struct_bases=[],
    name_mapping={
        "archive_extraction": "archiveExtraction",
        "dpkg_installation": "dpkgInstallation",
        "file_copy": "fileCopy",
        "file_exec": "fileExec",
        "msi_installation": "msiInstallation",
        "rpm_installation": "rpmInstallation",
        "script_run": "scriptRun",
    },
)
class GoogleOsConfigGuestPoliciesRecipesInstallSteps:
    def __init__(
        self,
        *,
        archive_extraction: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction", typing.Dict[builtins.str, typing.Any]]] = None,
        dpkg_installation: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation", typing.Dict[builtins.str, typing.Any]]] = None,
        file_copy: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy", typing.Dict[builtins.str, typing.Any]]] = None,
        file_exec: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec", typing.Dict[builtins.str, typing.Any]]] = None,
        msi_installation: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation", typing.Dict[builtins.str, typing.Any]]] = None,
        rpm_installation: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation", typing.Dict[builtins.str, typing.Any]]] = None,
        script_run: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param archive_extraction: archive_extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#archive_extraction GoogleOsConfigGuestPolicies#archive_extraction}
        :param dpkg_installation: dpkg_installation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#dpkg_installation GoogleOsConfigGuestPolicies#dpkg_installation}
        :param file_copy: file_copy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#file_copy GoogleOsConfigGuestPolicies#file_copy}
        :param file_exec: file_exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#file_exec GoogleOsConfigGuestPolicies#file_exec}
        :param msi_installation: msi_installation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#msi_installation GoogleOsConfigGuestPolicies#msi_installation}
        :param rpm_installation: rpm_installation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#rpm_installation GoogleOsConfigGuestPolicies#rpm_installation}
        :param script_run: script_run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#script_run GoogleOsConfigGuestPolicies#script_run}
        '''
        if isinstance(archive_extraction, dict):
            archive_extraction = GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction(**archive_extraction)
        if isinstance(dpkg_installation, dict):
            dpkg_installation = GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation(**dpkg_installation)
        if isinstance(file_copy, dict):
            file_copy = GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy(**file_copy)
        if isinstance(file_exec, dict):
            file_exec = GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec(**file_exec)
        if isinstance(msi_installation, dict):
            msi_installation = GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation(**msi_installation)
        if isinstance(rpm_installation, dict):
            rpm_installation = GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation(**rpm_installation)
        if isinstance(script_run, dict):
            script_run = GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun(**script_run)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d0ec2a66304470024f2638f2d7d728098c40aee50ae3bb1afa633f952fae8b)
            check_type(argname="argument archive_extraction", value=archive_extraction, expected_type=type_hints["archive_extraction"])
            check_type(argname="argument dpkg_installation", value=dpkg_installation, expected_type=type_hints["dpkg_installation"])
            check_type(argname="argument file_copy", value=file_copy, expected_type=type_hints["file_copy"])
            check_type(argname="argument file_exec", value=file_exec, expected_type=type_hints["file_exec"])
            check_type(argname="argument msi_installation", value=msi_installation, expected_type=type_hints["msi_installation"])
            check_type(argname="argument rpm_installation", value=rpm_installation, expected_type=type_hints["rpm_installation"])
            check_type(argname="argument script_run", value=script_run, expected_type=type_hints["script_run"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if archive_extraction is not None:
            self._values["archive_extraction"] = archive_extraction
        if dpkg_installation is not None:
            self._values["dpkg_installation"] = dpkg_installation
        if file_copy is not None:
            self._values["file_copy"] = file_copy
        if file_exec is not None:
            self._values["file_exec"] = file_exec
        if msi_installation is not None:
            self._values["msi_installation"] = msi_installation
        if rpm_installation is not None:
            self._values["rpm_installation"] = rpm_installation
        if script_run is not None:
            self._values["script_run"] = script_run

    @builtins.property
    def archive_extraction(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction"]:
        '''archive_extraction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#archive_extraction GoogleOsConfigGuestPolicies#archive_extraction}
        '''
        result = self._values.get("archive_extraction")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction"], result)

    @builtins.property
    def dpkg_installation(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation"]:
        '''dpkg_installation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#dpkg_installation GoogleOsConfigGuestPolicies#dpkg_installation}
        '''
        result = self._values.get("dpkg_installation")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation"], result)

    @builtins.property
    def file_copy(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy"]:
        '''file_copy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#file_copy GoogleOsConfigGuestPolicies#file_copy}
        '''
        result = self._values.get("file_copy")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy"], result)

    @builtins.property
    def file_exec(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec"]:
        '''file_exec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#file_exec GoogleOsConfigGuestPolicies#file_exec}
        '''
        result = self._values.get("file_exec")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec"], result)

    @builtins.property
    def msi_installation(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation"]:
        '''msi_installation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#msi_installation GoogleOsConfigGuestPolicies#msi_installation}
        '''
        result = self._values.get("msi_installation")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation"], result)

    @builtins.property
    def rpm_installation(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation"]:
        '''rpm_installation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#rpm_installation GoogleOsConfigGuestPolicies#rpm_installation}
        '''
        result = self._values.get("rpm_installation")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation"], result)

    @builtins.property
    def script_run(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun"]:
        '''script_run block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#script_run GoogleOsConfigGuestPolicies#script_run}
        '''
        result = self._values.get("script_run")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesInstallSteps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_id": "artifactId",
        "type": "type",
        "destination": "destination",
    },
)
class GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction:
    def __init__(
        self,
        *,
        artifact_id: builtins.str,
        type: builtins.str,
        destination: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param type: The type of the archive to extract. Possible values: ["TAR", "TAR_GZIP", "TAR_BZIP", "TAR_LZMA", "TAR_XZ", "ZIP"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#type GoogleOsConfigGuestPolicies#type}
        :param destination: Directory to extract archive to. Defaults to / on Linux or C:\\ on Windows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#destination GoogleOsConfigGuestPolicies#destination}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5ca3cd58b8731976c4d5f2e13907ce8afbf335bc3a1eb6933ff3095a5a32be7)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_id": artifact_id,
            "type": type,
        }
        if destination is not None:
            self._values["destination"] = destination

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''The id of the relevant artifact in the recipe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the archive to extract. Possible values: ["TAR", "TAR_GZIP", "TAR_BZIP", "TAR_LZMA", "TAR_XZ", "ZIP"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#type GoogleOsConfigGuestPolicies#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination(self) -> typing.Optional[builtins.str]:
        '''Directory to extract archive to. Defaults to / on Linux or C:\\ on Windows.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#destination GoogleOsConfigGuestPolicies#destination}
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtractionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtractionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47acd88987442dfcc94191deff663833b219052d96bd83d2c9e76a033fee60fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDestination")
    def reset_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestination", []))

    @builtins.property
    @jsii.member(jsii_name="artifactIdInput")
    def artifact_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @artifact_id.setter
    def artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__454069613145940f3762d791da8f6a6645a816c7b582e7eca9e3f9a5bbcf28bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6177dad4f43dc7a35401cfab0500bce8396599adcf5058a58864530c692acf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c70fd23136f1a8ce72b093de97a1d90d6e687470531d01f477d5c238574d36ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39288e6b29d8968b5dd24f5a5522a020234cf2b2e974d95a59c05b67d284a3b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation",
    jsii_struct_bases=[],
    name_mapping={"artifact_id": "artifactId"},
)
class GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation:
    def __init__(self, *, artifact_id: builtins.str) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8930b3fb3ab2d5481c0ba8afc67e0c823b7e4e62b9ec0916a097a8580343c544)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_id": artifact_id,
        }

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''The id of the relevant artifact in the recipe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5dd591284c4cd1d0e5c0d32496ac6273c345c8e1819c1fa52a12ff9f21b65f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="artifactIdInput")
    def artifact_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @artifact_id.setter
    def artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e362f9c047b27c709b6ec46dd5202f9c0178ceb37fe4b4598e2b3cf798ea9845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13303b027026e51736c59fafd7c5fab268c2847e10f73f0f737ebc8063f505f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_id": "artifactId",
        "destination": "destination",
        "overwrite": "overwrite",
        "permissions": "permissions",
    },
)
class GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy:
    def __init__(
        self,
        *,
        artifact_id: builtins.str,
        destination: builtins.str,
        overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param destination: The absolute path on the instance to put the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#destination GoogleOsConfigGuestPolicies#destination}
        :param overwrite: Whether to allow this step to overwrite existing files.If this is false and the file already exists the file is not overwritten and the step is considered a success. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#overwrite GoogleOsConfigGuestPolicies#overwrite}
        :param permissions: Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility). Each digit represents a three bit number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one bit corresponds to the execute permission. Default behavior is 755. Below are some examples of permissions and their associated values: read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#permissions GoogleOsConfigGuestPolicies#permissions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316217a9fb30acdd86db1a8c16184dc6c1efd212398444798f2773613359c6b2)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument overwrite", value=overwrite, expected_type=type_hints["overwrite"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_id": artifact_id,
            "destination": destination,
        }
        if overwrite is not None:
            self._values["overwrite"] = overwrite
        if permissions is not None:
            self._values["permissions"] = permissions

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''The id of the relevant artifact in the recipe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination(self) -> builtins.str:
        '''The absolute path on the instance to put the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#destination GoogleOsConfigGuestPolicies#destination}
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def overwrite(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow this step to overwrite existing files.If this is false and the file already exists the file is not overwritten and the step is considered a success. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#overwrite GoogleOsConfigGuestPolicies#overwrite}
        '''
        result = self._values.get("overwrite")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def permissions(self) -> typing.Optional[builtins.str]:
        '''Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility).

        Each digit represents a three bit
        number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one
        bit corresponds to the execute permission. Default behavior is 755.

        Below are some examples of permissions and their associated values:
        read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#permissions GoogleOsConfigGuestPolicies#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4b6f887d82c99087d88180e9bdc77046b4b6dcfc4fe8ef89aa53bb9dfb99748)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOverwrite")
    def reset_overwrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwrite", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @builtins.property
    @jsii.member(jsii_name="artifactIdInput")
    def artifact_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteInput")
    def overwrite_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overwriteInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @artifact_id.setter
    def artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd46b1d1d16d04896fff552e646114477cc42e58eb7fe14751e895a1af0edf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e9a01ca2a79256e117e9c0f543c022135e930eb9dc41ce00237b9c086c4036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwrite")
    def overwrite(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overwrite"))

    @overwrite.setter
    def overwrite(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a523da96f08eb0c7f2a796bf5c0aa58a950776f503ed79bf82721612761a3eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394abc0e0d85fc181db8840c4324c86a3060e36ac0af0592d5bbe222a26f03b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1623a32248b5b051ef881ae35f38151fb068502bdddb28b2eb3e2ffd1917c9bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_exit_codes": "allowedExitCodes",
        "args": "args",
        "artifact_id": "artifactId",
        "local_path": "localPath",
    },
)
class GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec:
    def __init__(
        self,
        *,
        allowed_exit_codes: typing.Optional[builtins.str] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        artifact_id: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_exit_codes: A list of possible return values that the program can return to indicate a success. Defaults to [0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        :param args: Arguments to be passed to the provided executable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#args GoogleOsConfigGuestPolicies#args}
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param local_path: The absolute path of the file on the local filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#local_path GoogleOsConfigGuestPolicies#local_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45fee08a7291146b25c9841b2ec1e7d1554e013f69b09fb5f4a151d782e194c2)
            check_type(argname="argument allowed_exit_codes", value=allowed_exit_codes, expected_type=type_hints["allowed_exit_codes"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_exit_codes is not None:
            self._values["allowed_exit_codes"] = allowed_exit_codes
        if args is not None:
            self._values["args"] = args
        if artifact_id is not None:
            self._values["artifact_id"] = artifact_id
        if local_path is not None:
            self._values["local_path"] = local_path

    @builtins.property
    def allowed_exit_codes(self) -> typing.Optional[builtins.str]:
        '''A list of possible return values that the program can return to indicate a success. Defaults to [0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        '''
        result = self._values.get("allowed_exit_codes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Arguments to be passed to the provided executable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#args GoogleOsConfigGuestPolicies#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def artifact_id(self) -> typing.Optional[builtins.str]:
        '''The id of the relevant artifact in the recipe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        result = self._values.get("artifact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''The absolute path of the file on the local filesystem.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#local_path GoogleOsConfigGuestPolicies#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4e36c2fbed3589dda5a1a7db12bc796edb3b234a04fcd0b28913fc81e47e206)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedExitCodes")
    def reset_allowed_exit_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedExitCodes", []))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetArtifactId")
    def reset_artifact_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArtifactId", []))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @builtins.property
    @jsii.member(jsii_name="allowedExitCodesInput")
    def allowed_exit_codes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowedExitCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactIdInput")
    def artifact_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedExitCodes")
    def allowed_exit_codes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowedExitCodes"))

    @allowed_exit_codes.setter
    def allowed_exit_codes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1329ba825bb8b0137869256e1a8a167e405a969be0fb322ee1a370f380e1326b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedExitCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda44815b858fb583d239b82b6bfd29e950b39532defe706d35c18087cb13dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @artifact_id.setter
    def artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03c978a4e6dce888058fae4e81f58139c5be49d77f55b460a655d2c8af0bdbce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e00ecbf9a0a3375293e94f7094cf5613f9ba9155144b91773ab59032cbbf073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4831a806ee62a13d2fec9df7f0a3be720c77c2b37d18a4e912e04b0ce3ad35a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesRecipesInstallStepsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90202a6642609e296db6b6347ad268ac8d1c7271599cf859a062a0be92126e13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigGuestPoliciesRecipesInstallStepsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9b8aa66541bacb5c2b3014664269819c0c31cb61d4d12e4ccf1fc98d452fbb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigGuestPoliciesRecipesInstallStepsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b2f2a398efa8c81d22ec59ea18ce96cb5c8fab02b5d3a3a501f8a3ee8e7120)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c33d429316ac18353d1bfa1568909bf6357187cc33c64ee442981e576a6ffbd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abec21655d6a3ee9adc5c90e38a4431eff57278fe3ea5f91f67b82d65593fde3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesInstallSteps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesInstallSteps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesInstallSteps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ceb5f9ea1362b9aafbc5be9515021b1bb5e72217577506bfe4840590116279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_id": "artifactId",
        "allowed_exit_codes": "allowedExitCodes",
        "flags": "flags",
    },
)
class GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation:
    def __init__(
        self,
        *,
        artifact_id: builtins.str,
        allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        flags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param allowed_exit_codes: Return codes that indicate that the software installed or updated successfully. Behaviour defaults to [0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        :param flags: The flags to use when installing the MSI. Defaults to the install flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#flags GoogleOsConfigGuestPolicies#flags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ac16d069e0c7f5e5292dba57b67f2e600060bc5712a98944ad51c3f9d3f43f)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument allowed_exit_codes", value=allowed_exit_codes, expected_type=type_hints["allowed_exit_codes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_id": artifact_id,
        }
        if allowed_exit_codes is not None:
            self._values["allowed_exit_codes"] = allowed_exit_codes
        if flags is not None:
            self._values["flags"] = flags

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''The id of the relevant artifact in the recipe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_exit_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Return codes that indicate that the software installed or updated successfully. Behaviour defaults to [0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        '''
        result = self._values.get("allowed_exit_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The flags to use when installing the MSI. Defaults to the install flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#flags GoogleOsConfigGuestPolicies#flags}
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2792d383245c76e0095c58e791346eb1cccaa712b89d4dfba8523b5d404df9af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedExitCodes")
    def reset_allowed_exit_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedExitCodes", []))

    @jsii.member(jsii_name="resetFlags")
    def reset_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlags", []))

    @builtins.property
    @jsii.member(jsii_name="allowedExitCodesInput")
    def allowed_exit_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowedExitCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactIdInput")
    def artifact_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdInput"))

    @builtins.property
    @jsii.member(jsii_name="flagsInput")
    def flags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "flagsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedExitCodes")
    def allowed_exit_codes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "allowedExitCodes"))

    @allowed_exit_codes.setter
    def allowed_exit_codes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__814b03b35eebdbeb6bf4fa69e5be4f9479ae9fc20277b0460e10107490ac0b2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedExitCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @artifact_id.setter
    def artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865b534b9fa7b60fe015cb4e01abe1c97ce45a164f476beb2bb5575ee2ae007c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flags")
    def flags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "flags"))

    @flags.setter
    def flags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50bf95c9851f23379f2adf38d0ce210c5b0e6686e12722075329c2f3c0eca29d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0cfbc5218e14e779917ff05f90fc99b49e419f5c10783b727c15b79a9a25e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesRecipesInstallStepsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45c8930bdb87751a14d527cbfe1faf0dfb59583b193250cc50d01d2d993fac13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putArchiveExtraction")
    def put_archive_extraction(
        self,
        *,
        artifact_id: builtins.str,
        type: builtins.str,
        destination: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param type: The type of the archive to extract. Possible values: ["TAR", "TAR_GZIP", "TAR_BZIP", "TAR_LZMA", "TAR_XZ", "ZIP"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#type GoogleOsConfigGuestPolicies#type}
        :param destination: Directory to extract archive to. Defaults to / on Linux or C:\\ on Windows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#destination GoogleOsConfigGuestPolicies#destination}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction(
            artifact_id=artifact_id, type=type, destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putArchiveExtraction", [value]))

    @jsii.member(jsii_name="putDpkgInstallation")
    def put_dpkg_installation(self, *, artifact_id: builtins.str) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation(
            artifact_id=artifact_id
        )

        return typing.cast(None, jsii.invoke(self, "putDpkgInstallation", [value]))

    @jsii.member(jsii_name="putFileCopy")
    def put_file_copy(
        self,
        *,
        artifact_id: builtins.str,
        destination: builtins.str,
        overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param destination: The absolute path on the instance to put the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#destination GoogleOsConfigGuestPolicies#destination}
        :param overwrite: Whether to allow this step to overwrite existing files.If this is false and the file already exists the file is not overwritten and the step is considered a success. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#overwrite GoogleOsConfigGuestPolicies#overwrite}
        :param permissions: Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility). Each digit represents a three bit number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one bit corresponds to the execute permission. Default behavior is 755. Below are some examples of permissions and their associated values: read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#permissions GoogleOsConfigGuestPolicies#permissions}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy(
            artifact_id=artifact_id,
            destination=destination,
            overwrite=overwrite,
            permissions=permissions,
        )

        return typing.cast(None, jsii.invoke(self, "putFileCopy", [value]))

    @jsii.member(jsii_name="putFileExec")
    def put_file_exec(
        self,
        *,
        allowed_exit_codes: typing.Optional[builtins.str] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        artifact_id: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_exit_codes: A list of possible return values that the program can return to indicate a success. Defaults to [0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        :param args: Arguments to be passed to the provided executable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#args GoogleOsConfigGuestPolicies#args}
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param local_path: The absolute path of the file on the local filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#local_path GoogleOsConfigGuestPolicies#local_path}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec(
            allowed_exit_codes=allowed_exit_codes,
            args=args,
            artifact_id=artifact_id,
            local_path=local_path,
        )

        return typing.cast(None, jsii.invoke(self, "putFileExec", [value]))

    @jsii.member(jsii_name="putMsiInstallation")
    def put_msi_installation(
        self,
        *,
        artifact_id: builtins.str,
        allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        flags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param allowed_exit_codes: Return codes that indicate that the software installed or updated successfully. Behaviour defaults to [0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        :param flags: The flags to use when installing the MSI. Defaults to the install flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#flags GoogleOsConfigGuestPolicies#flags}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation(
            artifact_id=artifact_id, allowed_exit_codes=allowed_exit_codes, flags=flags
        )

        return typing.cast(None, jsii.invoke(self, "putMsiInstallation", [value]))

    @jsii.member(jsii_name="putRpmInstallation")
    def put_rpm_installation(self, *, artifact_id: builtins.str) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation(
            artifact_id=artifact_id
        )

        return typing.cast(None, jsii.invoke(self, "putRpmInstallation", [value]))

    @jsii.member(jsii_name="putScriptRun")
    def put_script_run(
        self,
        *,
        script: builtins.str,
        allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        interpreter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param script: The shell script to be executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#script GoogleOsConfigGuestPolicies#script}
        :param allowed_exit_codes: Return codes that indicate that the software installed or updated successfully. Behaviour defaults to [0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script is executed directly, which likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#interpreter GoogleOsConfigGuestPolicies#interpreter}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun(
            script=script,
            allowed_exit_codes=allowed_exit_codes,
            interpreter=interpreter,
        )

        return typing.cast(None, jsii.invoke(self, "putScriptRun", [value]))

    @jsii.member(jsii_name="resetArchiveExtraction")
    def reset_archive_extraction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveExtraction", []))

    @jsii.member(jsii_name="resetDpkgInstallation")
    def reset_dpkg_installation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDpkgInstallation", []))

    @jsii.member(jsii_name="resetFileCopy")
    def reset_file_copy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileCopy", []))

    @jsii.member(jsii_name="resetFileExec")
    def reset_file_exec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileExec", []))

    @jsii.member(jsii_name="resetMsiInstallation")
    def reset_msi_installation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMsiInstallation", []))

    @jsii.member(jsii_name="resetRpmInstallation")
    def reset_rpm_installation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRpmInstallation", []))

    @jsii.member(jsii_name="resetScriptRun")
    def reset_script_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptRun", []))

    @builtins.property
    @jsii.member(jsii_name="archiveExtraction")
    def archive_extraction(
        self,
    ) -> GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtractionOutputReference:
        return typing.cast(GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtractionOutputReference, jsii.get(self, "archiveExtraction"))

    @builtins.property
    @jsii.member(jsii_name="dpkgInstallation")
    def dpkg_installation(
        self,
    ) -> GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallationOutputReference:
        return typing.cast(GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallationOutputReference, jsii.get(self, "dpkgInstallation"))

    @builtins.property
    @jsii.member(jsii_name="fileCopy")
    def file_copy(
        self,
    ) -> GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopyOutputReference:
        return typing.cast(GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopyOutputReference, jsii.get(self, "fileCopy"))

    @builtins.property
    @jsii.member(jsii_name="fileExec")
    def file_exec(
        self,
    ) -> GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExecOutputReference:
        return typing.cast(GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExecOutputReference, jsii.get(self, "fileExec"))

    @builtins.property
    @jsii.member(jsii_name="msiInstallation")
    def msi_installation(
        self,
    ) -> GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallationOutputReference:
        return typing.cast(GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallationOutputReference, jsii.get(self, "msiInstallation"))

    @builtins.property
    @jsii.member(jsii_name="rpmInstallation")
    def rpm_installation(
        self,
    ) -> "GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallationOutputReference":
        return typing.cast("GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallationOutputReference", jsii.get(self, "rpmInstallation"))

    @builtins.property
    @jsii.member(jsii_name="scriptRun")
    def script_run(
        self,
    ) -> "GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRunOutputReference":
        return typing.cast("GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRunOutputReference", jsii.get(self, "scriptRun"))

    @builtins.property
    @jsii.member(jsii_name="archiveExtractionInput")
    def archive_extraction_input(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction], jsii.get(self, "archiveExtractionInput"))

    @builtins.property
    @jsii.member(jsii_name="dpkgInstallationInput")
    def dpkg_installation_input(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation], jsii.get(self, "dpkgInstallationInput"))

    @builtins.property
    @jsii.member(jsii_name="fileCopyInput")
    def file_copy_input(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy], jsii.get(self, "fileCopyInput"))

    @builtins.property
    @jsii.member(jsii_name="fileExecInput")
    def file_exec_input(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec], jsii.get(self, "fileExecInput"))

    @builtins.property
    @jsii.member(jsii_name="msiInstallationInput")
    def msi_installation_input(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation], jsii.get(self, "msiInstallationInput"))

    @builtins.property
    @jsii.member(jsii_name="rpmInstallationInput")
    def rpm_installation_input(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation"]:
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation"], jsii.get(self, "rpmInstallationInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptRunInput")
    def script_run_input(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun"]:
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun"], jsii.get(self, "scriptRunInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipesInstallSteps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipesInstallSteps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipesInstallSteps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48142a1d25aa837cb4cbfa399fdc16e4dfd8100b954b03ac881789722fb1708c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation",
    jsii_struct_bases=[],
    name_mapping={"artifact_id": "artifactId"},
)
class GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation:
    def __init__(self, *, artifact_id: builtins.str) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e56938619bd8dfe48d15a232f9cfed71e7db767c5a50ed05fbe9ac4a34bd26fd)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_id": artifact_id,
        }

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''The id of the relevant artifact in the recipe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbac15be9f0c32ade9ffada18947ae3daeb2a5efa89c4cf5893a12580c5fea42)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="artifactIdInput")
    def artifact_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @artifact_id.setter
    def artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e8b491c0c81ccfb0418773266bc95baee7357310364711db91c7726e33c0f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c40018c0f36d2ee32f891c0f1352ba63a881719dba88b64acd1bcc0f0251175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun",
    jsii_struct_bases=[],
    name_mapping={
        "script": "script",
        "allowed_exit_codes": "allowedExitCodes",
        "interpreter": "interpreter",
    },
)
class GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun:
    def __init__(
        self,
        *,
        script: builtins.str,
        allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        interpreter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param script: The shell script to be executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#script GoogleOsConfigGuestPolicies#script}
        :param allowed_exit_codes: Return codes that indicate that the software installed or updated successfully. Behaviour defaults to [0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script is executed directly, which likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#interpreter GoogleOsConfigGuestPolicies#interpreter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a702921d59ee78169e401e97fec34d150d7f0c2012956bc8f7a115101a4c835f)
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument allowed_exit_codes", value=allowed_exit_codes, expected_type=type_hints["allowed_exit_codes"])
            check_type(argname="argument interpreter", value=interpreter, expected_type=type_hints["interpreter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "script": script,
        }
        if allowed_exit_codes is not None:
            self._values["allowed_exit_codes"] = allowed_exit_codes
        if interpreter is not None:
            self._values["interpreter"] = interpreter

    @builtins.property
    def script(self) -> builtins.str:
        '''The shell script to be executed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#script GoogleOsConfigGuestPolicies#script}
        '''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_exit_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Return codes that indicate that the software installed or updated successfully. Behaviour defaults to [0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        '''
        result = self._values.get("allowed_exit_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def interpreter(self) -> typing.Optional[builtins.str]:
        '''The script interpreter to use to run the script.

        If no interpreter is specified the script is executed directly,
        which likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#interpreter GoogleOsConfigGuestPolicies#interpreter}
        '''
        result = self._values.get("interpreter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRunOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRunOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d048cde5518a2c86da144318357d50c5d84cfdbb4634ea39d9bcec483297374)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedExitCodes")
    def reset_allowed_exit_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedExitCodes", []))

    @jsii.member(jsii_name="resetInterpreter")
    def reset_interpreter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterpreter", []))

    @builtins.property
    @jsii.member(jsii_name="allowedExitCodesInput")
    def allowed_exit_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowedExitCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="interpreterInput")
    def interpreter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interpreterInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptInput")
    def script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedExitCodes")
    def allowed_exit_codes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "allowedExitCodes"))

    @allowed_exit_codes.setter
    def allowed_exit_codes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87c77cef6b50735b1f45f57130b5af00e8d1d56e5504822077278fb509dff9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedExitCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ba25a4e3729026caa750888c54a1f053b795cb7cd925ce4affedc0d0b3eda7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54660dec1cc29e9e55e3c1418be2c2b4c750375d103238602ff1a42f66eb79f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e5e8a545848c85798a2d42e91b626d8cdd17022b072b7c674d97e86b77a716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesRecipesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95ea35f3a8d8301247e8f84f5f5e10ac7aeef3449f38d70a3ec62d7fb447b8e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigGuestPoliciesRecipesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68f292a02d2fcc5f3b93dbf65c1e1d5a1d24c70f8f02ed7cd5fac1fc54aecb69)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigGuestPoliciesRecipesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__983b15e869ffe2f1e092eebb0b8448abbbfdc2e925a3385857439e20c4e38b1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79352c878149b3902405493326d71403b6b2f1d910b7809639cd12460fc48395)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8fda1d4ed4b354a3ec54bb7d0c933f1ffdcb45f8aec25ffd04c300744d8b319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c05548bb1af2eeebf8f739575fc91c0b6028542910ff74757dba4746c7c1e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesRecipesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d10e8595f6d417b1c8b86005cfcd1985b31c0c930fd0b7ef84802f090729521)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putArtifacts")
    def put_artifacts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesRecipesArtifacts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4d7d28c6691e109626b46c667989816e90be5605ec80b272c2d451e612445c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArtifacts", [value]))

    @jsii.member(jsii_name="putInstallSteps")
    def put_install_steps(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesRecipesInstallSteps, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f9e7ddecdf30fef8dae40af2cc38ab564d22e83a223a00127c65741f015e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInstallSteps", [value]))

    @jsii.member(jsii_name="putUpdateSteps")
    def put_update_steps(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigGuestPoliciesRecipesUpdateSteps", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cec13c6a7f3e818ac0704dd604fb1d3eb590edfb22619e990072aceecb9c137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUpdateSteps", [value]))

    @jsii.member(jsii_name="resetArtifacts")
    def reset_artifacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArtifacts", []))

    @jsii.member(jsii_name="resetDesiredState")
    def reset_desired_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredState", []))

    @jsii.member(jsii_name="resetInstallSteps")
    def reset_install_steps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstallSteps", []))

    @jsii.member(jsii_name="resetUpdateSteps")
    def reset_update_steps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateSteps", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> GoogleOsConfigGuestPoliciesRecipesArtifactsList:
        return typing.cast(GoogleOsConfigGuestPoliciesRecipesArtifactsList, jsii.get(self, "artifacts"))

    @builtins.property
    @jsii.member(jsii_name="installSteps")
    def install_steps(self) -> GoogleOsConfigGuestPoliciesRecipesInstallStepsList:
        return typing.cast(GoogleOsConfigGuestPoliciesRecipesInstallStepsList, jsii.get(self, "installSteps"))

    @builtins.property
    @jsii.member(jsii_name="updateSteps")
    def update_steps(self) -> "GoogleOsConfigGuestPoliciesRecipesUpdateStepsList":
        return typing.cast("GoogleOsConfigGuestPoliciesRecipesUpdateStepsList", jsii.get(self, "updateSteps"))

    @builtins.property
    @jsii.member(jsii_name="artifactsInput")
    def artifacts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesArtifacts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesArtifacts]]], jsii.get(self, "artifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="installStepsInput")
    def install_steps_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesInstallSteps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesInstallSteps]]], jsii.get(self, "installStepsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="updateStepsInput")
    def update_steps_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesRecipesUpdateSteps"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigGuestPoliciesRecipesUpdateSteps"]]], jsii.get(self, "updateStepsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c82f8d9d4390004059633f28fb3b34ff73ba72bc3f8e383316bb5439bc92de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77460f8ad86afec7ede7ccac4bcfa0b7e9dd212b158f64403aa97110120582e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc869115cbf2694425b7099c114caeab78d17f5bc10b33a231329a17f04ed953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643875c8a78be33983c4a76de8c8ab4e83bf34f6e55aa2396529ac87e8a27262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateSteps",
    jsii_struct_bases=[],
    name_mapping={
        "archive_extraction": "archiveExtraction",
        "dpkg_installation": "dpkgInstallation",
        "file_copy": "fileCopy",
        "file_exec": "fileExec",
        "msi_installation": "msiInstallation",
        "rpm_installation": "rpmInstallation",
        "script_run": "scriptRun",
    },
)
class GoogleOsConfigGuestPoliciesRecipesUpdateSteps:
    def __init__(
        self,
        *,
        archive_extraction: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction", typing.Dict[builtins.str, typing.Any]]] = None,
        dpkg_installation: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation", typing.Dict[builtins.str, typing.Any]]] = None,
        file_copy: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy", typing.Dict[builtins.str, typing.Any]]] = None,
        file_exec: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec", typing.Dict[builtins.str, typing.Any]]] = None,
        msi_installation: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation", typing.Dict[builtins.str, typing.Any]]] = None,
        rpm_installation: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation", typing.Dict[builtins.str, typing.Any]]] = None,
        script_run: typing.Optional[typing.Union["GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param archive_extraction: archive_extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#archive_extraction GoogleOsConfigGuestPolicies#archive_extraction}
        :param dpkg_installation: dpkg_installation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#dpkg_installation GoogleOsConfigGuestPolicies#dpkg_installation}
        :param file_copy: file_copy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#file_copy GoogleOsConfigGuestPolicies#file_copy}
        :param file_exec: file_exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#file_exec GoogleOsConfigGuestPolicies#file_exec}
        :param msi_installation: msi_installation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#msi_installation GoogleOsConfigGuestPolicies#msi_installation}
        :param rpm_installation: rpm_installation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#rpm_installation GoogleOsConfigGuestPolicies#rpm_installation}
        :param script_run: script_run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#script_run GoogleOsConfigGuestPolicies#script_run}
        '''
        if isinstance(archive_extraction, dict):
            archive_extraction = GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction(**archive_extraction)
        if isinstance(dpkg_installation, dict):
            dpkg_installation = GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation(**dpkg_installation)
        if isinstance(file_copy, dict):
            file_copy = GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy(**file_copy)
        if isinstance(file_exec, dict):
            file_exec = GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec(**file_exec)
        if isinstance(msi_installation, dict):
            msi_installation = GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation(**msi_installation)
        if isinstance(rpm_installation, dict):
            rpm_installation = GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation(**rpm_installation)
        if isinstance(script_run, dict):
            script_run = GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun(**script_run)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef10b2c8ce8b11ddfe3bb3aa235a5442ba8d18409da9553443bce2d04001e0d0)
            check_type(argname="argument archive_extraction", value=archive_extraction, expected_type=type_hints["archive_extraction"])
            check_type(argname="argument dpkg_installation", value=dpkg_installation, expected_type=type_hints["dpkg_installation"])
            check_type(argname="argument file_copy", value=file_copy, expected_type=type_hints["file_copy"])
            check_type(argname="argument file_exec", value=file_exec, expected_type=type_hints["file_exec"])
            check_type(argname="argument msi_installation", value=msi_installation, expected_type=type_hints["msi_installation"])
            check_type(argname="argument rpm_installation", value=rpm_installation, expected_type=type_hints["rpm_installation"])
            check_type(argname="argument script_run", value=script_run, expected_type=type_hints["script_run"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if archive_extraction is not None:
            self._values["archive_extraction"] = archive_extraction
        if dpkg_installation is not None:
            self._values["dpkg_installation"] = dpkg_installation
        if file_copy is not None:
            self._values["file_copy"] = file_copy
        if file_exec is not None:
            self._values["file_exec"] = file_exec
        if msi_installation is not None:
            self._values["msi_installation"] = msi_installation
        if rpm_installation is not None:
            self._values["rpm_installation"] = rpm_installation
        if script_run is not None:
            self._values["script_run"] = script_run

    @builtins.property
    def archive_extraction(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction"]:
        '''archive_extraction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#archive_extraction GoogleOsConfigGuestPolicies#archive_extraction}
        '''
        result = self._values.get("archive_extraction")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction"], result)

    @builtins.property
    def dpkg_installation(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation"]:
        '''dpkg_installation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#dpkg_installation GoogleOsConfigGuestPolicies#dpkg_installation}
        '''
        result = self._values.get("dpkg_installation")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation"], result)

    @builtins.property
    def file_copy(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy"]:
        '''file_copy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#file_copy GoogleOsConfigGuestPolicies#file_copy}
        '''
        result = self._values.get("file_copy")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy"], result)

    @builtins.property
    def file_exec(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec"]:
        '''file_exec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#file_exec GoogleOsConfigGuestPolicies#file_exec}
        '''
        result = self._values.get("file_exec")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec"], result)

    @builtins.property
    def msi_installation(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation"]:
        '''msi_installation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#msi_installation GoogleOsConfigGuestPolicies#msi_installation}
        '''
        result = self._values.get("msi_installation")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation"], result)

    @builtins.property
    def rpm_installation(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation"]:
        '''rpm_installation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#rpm_installation GoogleOsConfigGuestPolicies#rpm_installation}
        '''
        result = self._values.get("rpm_installation")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation"], result)

    @builtins.property
    def script_run(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun"]:
        '''script_run block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#script_run GoogleOsConfigGuestPolicies#script_run}
        '''
        result = self._values.get("script_run")
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesUpdateSteps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_id": "artifactId",
        "type": "type",
        "destination": "destination",
    },
)
class GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction:
    def __init__(
        self,
        *,
        artifact_id: builtins.str,
        type: builtins.str,
        destination: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param type: The type of the archive to extract. Possible values: ["TAR", "TAR_GZIP", "TAR_BZIP", "TAR_LZMA", "TAR_XZ", "ZIP"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#type GoogleOsConfigGuestPolicies#type}
        :param destination: Directory to extract archive to. Defaults to / on Linux or C:\\ on Windows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#destination GoogleOsConfigGuestPolicies#destination}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11170ff88e4945521d1431a1cf4bb2e23468cb6cabb00e9c8388032d3630a4b4)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_id": artifact_id,
            "type": type,
        }
        if destination is not None:
            self._values["destination"] = destination

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''The id of the relevant artifact in the recipe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the archive to extract. Possible values: ["TAR", "TAR_GZIP", "TAR_BZIP", "TAR_LZMA", "TAR_XZ", "ZIP"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#type GoogleOsConfigGuestPolicies#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination(self) -> typing.Optional[builtins.str]:
        '''Directory to extract archive to. Defaults to / on Linux or C:\\ on Windows.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#destination GoogleOsConfigGuestPolicies#destination}
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtractionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtractionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc39e1bde116761569964a814b49e7f9a205cfa31bb726afccfc2fdbf984301a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDestination")
    def reset_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestination", []))

    @builtins.property
    @jsii.member(jsii_name="artifactIdInput")
    def artifact_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @artifact_id.setter
    def artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d4ea8fab62496ae765e56c2c421d6494d53d005dea5bd2f2de1e614a4c43545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df5535da7b703d0d78d841ece92c3c919666b066e6aa692028a802759f58d22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b09528a968f292ea243f756a83be48c44d5b6ca2bd002dcce36a8fff67b3de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12bc3d501247ca017ec3ca1e575d7be083f16a107b7c9337dab737d052b2814b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation",
    jsii_struct_bases=[],
    name_mapping={"artifact_id": "artifactId"},
)
class GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation:
    def __init__(self, *, artifact_id: builtins.str) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f62c5cf8da5ed10a27f2198c3e8e8fb613edcb329ffe3f27c4e68531bdf2ef)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_id": artifact_id,
        }

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''The id of the relevant artifact in the recipe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ada181a7340e297108ced84e7df57a2058e7c4b93b3c8830b24e4bafacafd406)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="artifactIdInput")
    def artifact_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @artifact_id.setter
    def artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ad70ef4cbf333d81c32e0a0380e56b46d746848b142f2d1fbed0e525a9527e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea083ac3b99f23ad4c5bd58c48ce29427ad08c3bd6e44f1fc4b14d0f2e63a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_id": "artifactId",
        "destination": "destination",
        "overwrite": "overwrite",
        "permissions": "permissions",
    },
)
class GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy:
    def __init__(
        self,
        *,
        artifact_id: builtins.str,
        destination: builtins.str,
        overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param destination: The absolute path on the instance to put the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#destination GoogleOsConfigGuestPolicies#destination}
        :param overwrite: Whether to allow this step to overwrite existing files.If this is false and the file already exists the file is not overwritten and the step is considered a success. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#overwrite GoogleOsConfigGuestPolicies#overwrite}
        :param permissions: Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility). Each digit represents a three bit number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one bit corresponds to the execute permission. Default behavior is 755. Below are some examples of permissions and their associated values: read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#permissions GoogleOsConfigGuestPolicies#permissions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41080f970bb0586136d39018036a212139c2fb6f755fbe1b1a64dbb60a14749)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument overwrite", value=overwrite, expected_type=type_hints["overwrite"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_id": artifact_id,
            "destination": destination,
        }
        if overwrite is not None:
            self._values["overwrite"] = overwrite
        if permissions is not None:
            self._values["permissions"] = permissions

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''The id of the relevant artifact in the recipe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination(self) -> builtins.str:
        '''The absolute path on the instance to put the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#destination GoogleOsConfigGuestPolicies#destination}
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def overwrite(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow this step to overwrite existing files.If this is false and the file already exists the file is not overwritten and the step is considered a success. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#overwrite GoogleOsConfigGuestPolicies#overwrite}
        '''
        result = self._values.get("overwrite")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def permissions(self) -> typing.Optional[builtins.str]:
        '''Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility).

        Each digit represents a three bit
        number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one
        bit corresponds to the execute permission. Default behavior is 755.

        Below are some examples of permissions and their associated values:
        read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#permissions GoogleOsConfigGuestPolicies#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb2101fc6d94101344e823912783fdd82299e6dca3bfa33a762931bc28c566cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOverwrite")
    def reset_overwrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwrite", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @builtins.property
    @jsii.member(jsii_name="artifactIdInput")
    def artifact_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteInput")
    def overwrite_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overwriteInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @artifact_id.setter
    def artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068680c35cd5f0df22baf02ff2a43dbb045da5ff6f80e251067315eb9682cd56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944b6ae823e89210376f34d81221aad582578d8fd384307eb811283f935457e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwrite")
    def overwrite(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overwrite"))

    @overwrite.setter
    def overwrite(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42218a013a78163a99376e411bd1a0c26bc0f15fbb048b319e48db5b451d407e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c928e10a445f338c33ec130dd0bc7440d7ef7dcfae63171f95346385c00e51b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d52df47cea2578cda2874084a1689d4ef3b74112e51c6163ed4cbfe664a79b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_exit_codes": "allowedExitCodes",
        "args": "args",
        "artifact_id": "artifactId",
        "local_path": "localPath",
    },
)
class GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec:
    def __init__(
        self,
        *,
        allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        artifact_id: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_exit_codes: A list of possible return values that the program can return to indicate a success. Defaults to [0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        :param args: Arguments to be passed to the provided executable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#args GoogleOsConfigGuestPolicies#args}
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param local_path: The absolute path of the file on the local filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#local_path GoogleOsConfigGuestPolicies#local_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb00599a8cf774220ad1ceedd94bf53097349c407508c22b933f470a124913b3)
            check_type(argname="argument allowed_exit_codes", value=allowed_exit_codes, expected_type=type_hints["allowed_exit_codes"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_exit_codes is not None:
            self._values["allowed_exit_codes"] = allowed_exit_codes
        if args is not None:
            self._values["args"] = args
        if artifact_id is not None:
            self._values["artifact_id"] = artifact_id
        if local_path is not None:
            self._values["local_path"] = local_path

    @builtins.property
    def allowed_exit_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''A list of possible return values that the program can return to indicate a success. Defaults to [0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        '''
        result = self._values.get("allowed_exit_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Arguments to be passed to the provided executable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#args GoogleOsConfigGuestPolicies#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def artifact_id(self) -> typing.Optional[builtins.str]:
        '''The id of the relevant artifact in the recipe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        result = self._values.get("artifact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''The absolute path of the file on the local filesystem.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#local_path GoogleOsConfigGuestPolicies#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fe6764ec540c345fd3d271daabf25b7f8845c9fa09e2ea4d5e7c96389175067)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedExitCodes")
    def reset_allowed_exit_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedExitCodes", []))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetArtifactId")
    def reset_artifact_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArtifactId", []))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @builtins.property
    @jsii.member(jsii_name="allowedExitCodesInput")
    def allowed_exit_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowedExitCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactIdInput")
    def artifact_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedExitCodes")
    def allowed_exit_codes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "allowedExitCodes"))

    @allowed_exit_codes.setter
    def allowed_exit_codes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073b07736facc964e564702ff6bfdcf2f79fe7532f77eda6a7cbc6440771b1a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedExitCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6e35af1dbc3e6c6983e9e1158f9ec9bb5f547f5af694fcbf4b058e81768287)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @artifact_id.setter
    def artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__910d951a1ce6e5a1400254d26910e9401720fe30caa91ad4fbbd0a7101918c1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb1ae2009f3f0830d058a944de98f9570bbf34f0464cdfb6eae75ac652288ff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ff4ba25abe97386543b2a105e258e6097e9166fc2bd853447d4226f602710c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesRecipesUpdateStepsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d701cad627087c3a80f44531fb6082ccbd3c918d8c2ffd204f43b547b68dfa58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigGuestPoliciesRecipesUpdateStepsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95159a1607491ae73316e105db406e4dcd3e06405740353abc0968f7487787e6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigGuestPoliciesRecipesUpdateStepsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd4e5ca04b1d240889eabc0de859b11758d38920edb87d4eb676ad55994adf4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6054c8b0100d59c87a3ec43aa01cdceeef54eba2865bc588302d2fed6f45fab2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d53db2c3630fa47ba66ce21aa19c69e6802cf46c8db4aa5e7076ee3e7b10f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesUpdateSteps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesUpdateSteps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesUpdateSteps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f17ec533d71766f8313928166d08bdcb2259a179fed1359fdbbc6a83c8b7f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_id": "artifactId",
        "allowed_exit_codes": "allowedExitCodes",
        "flags": "flags",
    },
)
class GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation:
    def __init__(
        self,
        *,
        artifact_id: builtins.str,
        allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        flags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param allowed_exit_codes: Return codes that indicate that the software installed or updated successfully. Behaviour defaults to [0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        :param flags: The flags to use when installing the MSI. Defaults to the install flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#flags GoogleOsConfigGuestPolicies#flags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6404aa47814caef1830b9b61f76210ad5d26cd68c452b711451537acd7ced9)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument allowed_exit_codes", value=allowed_exit_codes, expected_type=type_hints["allowed_exit_codes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_id": artifact_id,
        }
        if allowed_exit_codes is not None:
            self._values["allowed_exit_codes"] = allowed_exit_codes
        if flags is not None:
            self._values["flags"] = flags

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''The id of the relevant artifact in the recipe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_exit_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Return codes that indicate that the software installed or updated successfully. Behaviour defaults to [0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        '''
        result = self._values.get("allowed_exit_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The flags to use when installing the MSI. Defaults to the install flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#flags GoogleOsConfigGuestPolicies#flags}
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19e9f4b8ec61e36421c8de28d04cd11edf7bfc34825ac45f7fec0d3a2f40fd1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedExitCodes")
    def reset_allowed_exit_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedExitCodes", []))

    @jsii.member(jsii_name="resetFlags")
    def reset_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlags", []))

    @builtins.property
    @jsii.member(jsii_name="allowedExitCodesInput")
    def allowed_exit_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowedExitCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactIdInput")
    def artifact_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdInput"))

    @builtins.property
    @jsii.member(jsii_name="flagsInput")
    def flags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "flagsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedExitCodes")
    def allowed_exit_codes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "allowedExitCodes"))

    @allowed_exit_codes.setter
    def allowed_exit_codes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7207a3d7196975bc47d2cdb6af7d222b46e880908189a0066125c5192a70b76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedExitCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @artifact_id.setter
    def artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11075d44291f50f881149bfa69d061ac26c0aa728c0ab19e85e60779d901a61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flags")
    def flags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "flags"))

    @flags.setter
    def flags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691c38303729396ea455d2a1ebc7770e3d5db59cc68abec39fad65e3c6350d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c8c20fb88a2d10cebae9c0aaeb94afe2a7d8e4fa2a2e6a9f1585d8014aada2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigGuestPoliciesRecipesUpdateStepsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20976fa817e4e19cbbc012f49f13e37e148e4a9318e812684a11f7ff87702c74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putArchiveExtraction")
    def put_archive_extraction(
        self,
        *,
        artifact_id: builtins.str,
        type: builtins.str,
        destination: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param type: The type of the archive to extract. Possible values: ["TAR", "TAR_GZIP", "TAR_BZIP", "TAR_LZMA", "TAR_XZ", "ZIP"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#type GoogleOsConfigGuestPolicies#type}
        :param destination: Directory to extract archive to. Defaults to / on Linux or C:\\ on Windows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#destination GoogleOsConfigGuestPolicies#destination}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction(
            artifact_id=artifact_id, type=type, destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putArchiveExtraction", [value]))

    @jsii.member(jsii_name="putDpkgInstallation")
    def put_dpkg_installation(self, *, artifact_id: builtins.str) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation(
            artifact_id=artifact_id
        )

        return typing.cast(None, jsii.invoke(self, "putDpkgInstallation", [value]))

    @jsii.member(jsii_name="putFileCopy")
    def put_file_copy(
        self,
        *,
        artifact_id: builtins.str,
        destination: builtins.str,
        overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param destination: The absolute path on the instance to put the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#destination GoogleOsConfigGuestPolicies#destination}
        :param overwrite: Whether to allow this step to overwrite existing files.If this is false and the file already exists the file is not overwritten and the step is considered a success. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#overwrite GoogleOsConfigGuestPolicies#overwrite}
        :param permissions: Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility). Each digit represents a three bit number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one bit corresponds to the execute permission. Default behavior is 755. Below are some examples of permissions and their associated values: read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#permissions GoogleOsConfigGuestPolicies#permissions}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy(
            artifact_id=artifact_id,
            destination=destination,
            overwrite=overwrite,
            permissions=permissions,
        )

        return typing.cast(None, jsii.invoke(self, "putFileCopy", [value]))

    @jsii.member(jsii_name="putFileExec")
    def put_file_exec(
        self,
        *,
        allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        artifact_id: typing.Optional[builtins.str] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_exit_codes: A list of possible return values that the program can return to indicate a success. Defaults to [0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        :param args: Arguments to be passed to the provided executable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#args GoogleOsConfigGuestPolicies#args}
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param local_path: The absolute path of the file on the local filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#local_path GoogleOsConfigGuestPolicies#local_path}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec(
            allowed_exit_codes=allowed_exit_codes,
            args=args,
            artifact_id=artifact_id,
            local_path=local_path,
        )

        return typing.cast(None, jsii.invoke(self, "putFileExec", [value]))

    @jsii.member(jsii_name="putMsiInstallation")
    def put_msi_installation(
        self,
        *,
        artifact_id: builtins.str,
        allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        flags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        :param allowed_exit_codes: Return codes that indicate that the software installed or updated successfully. Behaviour defaults to [0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        :param flags: The flags to use when installing the MSI. Defaults to the install flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#flags GoogleOsConfigGuestPolicies#flags}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation(
            artifact_id=artifact_id, allowed_exit_codes=allowed_exit_codes, flags=flags
        )

        return typing.cast(None, jsii.invoke(self, "putMsiInstallation", [value]))

    @jsii.member(jsii_name="putRpmInstallation")
    def put_rpm_installation(self, *, artifact_id: builtins.str) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation(
            artifact_id=artifact_id
        )

        return typing.cast(None, jsii.invoke(self, "putRpmInstallation", [value]))

    @jsii.member(jsii_name="putScriptRun")
    def put_script_run(
        self,
        *,
        script: builtins.str,
        allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        interpreter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param script: The shell script to be executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#script GoogleOsConfigGuestPolicies#script}
        :param allowed_exit_codes: Return codes that indicate that the software installed or updated successfully. Behaviour defaults to [0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script is executed directly, which likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#interpreter GoogleOsConfigGuestPolicies#interpreter}
        '''
        value = GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun(
            script=script,
            allowed_exit_codes=allowed_exit_codes,
            interpreter=interpreter,
        )

        return typing.cast(None, jsii.invoke(self, "putScriptRun", [value]))

    @jsii.member(jsii_name="resetArchiveExtraction")
    def reset_archive_extraction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveExtraction", []))

    @jsii.member(jsii_name="resetDpkgInstallation")
    def reset_dpkg_installation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDpkgInstallation", []))

    @jsii.member(jsii_name="resetFileCopy")
    def reset_file_copy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileCopy", []))

    @jsii.member(jsii_name="resetFileExec")
    def reset_file_exec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileExec", []))

    @jsii.member(jsii_name="resetMsiInstallation")
    def reset_msi_installation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMsiInstallation", []))

    @jsii.member(jsii_name="resetRpmInstallation")
    def reset_rpm_installation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRpmInstallation", []))

    @jsii.member(jsii_name="resetScriptRun")
    def reset_script_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptRun", []))

    @builtins.property
    @jsii.member(jsii_name="archiveExtraction")
    def archive_extraction(
        self,
    ) -> GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtractionOutputReference:
        return typing.cast(GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtractionOutputReference, jsii.get(self, "archiveExtraction"))

    @builtins.property
    @jsii.member(jsii_name="dpkgInstallation")
    def dpkg_installation(
        self,
    ) -> GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallationOutputReference:
        return typing.cast(GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallationOutputReference, jsii.get(self, "dpkgInstallation"))

    @builtins.property
    @jsii.member(jsii_name="fileCopy")
    def file_copy(
        self,
    ) -> GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopyOutputReference:
        return typing.cast(GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopyOutputReference, jsii.get(self, "fileCopy"))

    @builtins.property
    @jsii.member(jsii_name="fileExec")
    def file_exec(
        self,
    ) -> GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExecOutputReference:
        return typing.cast(GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExecOutputReference, jsii.get(self, "fileExec"))

    @builtins.property
    @jsii.member(jsii_name="msiInstallation")
    def msi_installation(
        self,
    ) -> GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallationOutputReference:
        return typing.cast(GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallationOutputReference, jsii.get(self, "msiInstallation"))

    @builtins.property
    @jsii.member(jsii_name="rpmInstallation")
    def rpm_installation(
        self,
    ) -> "GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallationOutputReference":
        return typing.cast("GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallationOutputReference", jsii.get(self, "rpmInstallation"))

    @builtins.property
    @jsii.member(jsii_name="scriptRun")
    def script_run(
        self,
    ) -> "GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRunOutputReference":
        return typing.cast("GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRunOutputReference", jsii.get(self, "scriptRun"))

    @builtins.property
    @jsii.member(jsii_name="archiveExtractionInput")
    def archive_extraction_input(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction], jsii.get(self, "archiveExtractionInput"))

    @builtins.property
    @jsii.member(jsii_name="dpkgInstallationInput")
    def dpkg_installation_input(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation], jsii.get(self, "dpkgInstallationInput"))

    @builtins.property
    @jsii.member(jsii_name="fileCopyInput")
    def file_copy_input(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy], jsii.get(self, "fileCopyInput"))

    @builtins.property
    @jsii.member(jsii_name="fileExecInput")
    def file_exec_input(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec], jsii.get(self, "fileExecInput"))

    @builtins.property
    @jsii.member(jsii_name="msiInstallationInput")
    def msi_installation_input(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation], jsii.get(self, "msiInstallationInput"))

    @builtins.property
    @jsii.member(jsii_name="rpmInstallationInput")
    def rpm_installation_input(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation"]:
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation"], jsii.get(self, "rpmInstallationInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptRunInput")
    def script_run_input(
        self,
    ) -> typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun"]:
        return typing.cast(typing.Optional["GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun"], jsii.get(self, "scriptRunInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipesUpdateSteps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipesUpdateSteps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipesUpdateSteps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c80be6f9bc726251f22aa525e0f51e5e849f70f665aa5c81ba134098e67cb1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation",
    jsii_struct_bases=[],
    name_mapping={"artifact_id": "artifactId"},
)
class GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation:
    def __init__(self, *, artifact_id: builtins.str) -> None:
        '''
        :param artifact_id: The id of the relevant artifact in the recipe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc08a3fce2d4bf4f009102a1dd39210ae263a3b26298a6cb3a1c7f62ec668fea)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_id": artifact_id,
        }

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''The id of the relevant artifact in the recipe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#artifact_id GoogleOsConfigGuestPolicies#artifact_id}
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__606b329f2d003aea77b3e777d01ddb55276adb86d62079b4662d948cd34cbedb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="artifactIdInput")
    def artifact_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactIdInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactId"))

    @artifact_id.setter
    def artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0776ee96fbc36b63974b2152434dfc11f33ede5b94d7466d2fda03242fb2a3b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf73d7a044bf1f8574258654e3700e887dfe4384bc40f875de745881105a9925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun",
    jsii_struct_bases=[],
    name_mapping={
        "script": "script",
        "allowed_exit_codes": "allowedExitCodes",
        "interpreter": "interpreter",
    },
)
class GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun:
    def __init__(
        self,
        *,
        script: builtins.str,
        allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        interpreter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param script: The shell script to be executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#script GoogleOsConfigGuestPolicies#script}
        :param allowed_exit_codes: Return codes that indicate that the software installed or updated successfully. Behaviour defaults to [0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        :param interpreter: The script interpreter to use to run the script. If no interpreter is specified the script is executed directly, which likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#interpreter GoogleOsConfigGuestPolicies#interpreter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d9871f623430f667bb61b9c9a7f42711cf2a40d3c4eed2f3323b11579d001a4)
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument allowed_exit_codes", value=allowed_exit_codes, expected_type=type_hints["allowed_exit_codes"])
            check_type(argname="argument interpreter", value=interpreter, expected_type=type_hints["interpreter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "script": script,
        }
        if allowed_exit_codes is not None:
            self._values["allowed_exit_codes"] = allowed_exit_codes
        if interpreter is not None:
            self._values["interpreter"] = interpreter

    @builtins.property
    def script(self) -> builtins.str:
        '''The shell script to be executed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#script GoogleOsConfigGuestPolicies#script}
        '''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_exit_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Return codes that indicate that the software installed or updated successfully. Behaviour defaults to [0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#allowed_exit_codes GoogleOsConfigGuestPolicies#allowed_exit_codes}
        '''
        result = self._values.get("allowed_exit_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def interpreter(self) -> typing.Optional[builtins.str]:
        '''The script interpreter to use to run the script.

        If no interpreter is specified the script is executed directly,
        which likely only succeed for scripts with shebang lines. Possible values: ["SHELL", "POWERSHELL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#interpreter GoogleOsConfigGuestPolicies#interpreter}
        '''
        result = self._values.get("interpreter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRunOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRunOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd3b3aa93281118b9037aca58d653ab2b7f4ee71a727c224c83e21e2cd2db40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedExitCodes")
    def reset_allowed_exit_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedExitCodes", []))

    @jsii.member(jsii_name="resetInterpreter")
    def reset_interpreter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterpreter", []))

    @builtins.property
    @jsii.member(jsii_name="allowedExitCodesInput")
    def allowed_exit_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "allowedExitCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="interpreterInput")
    def interpreter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interpreterInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptInput")
    def script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedExitCodes")
    def allowed_exit_codes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "allowedExitCodes"))

    @allowed_exit_codes.setter
    def allowed_exit_codes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__378f7fb38c35d49710496bdc10d6b2a61e22adccd6f7cb56abafb132077ef7df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedExitCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af948c4b3ca58d56a9bda1e92442279b5dfc8128954d16d8817e87ee74a7fb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74fc7a5ab42993561129d2e5e211e25ffc26327e81a88b4cc8dcbefa9cd92370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun]:
        return typing.cast(typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db6a25d0eeb29c10fbc171c476d01b96995a7e85837fafc85fa2528ba842de4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleOsConfigGuestPoliciesTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#create GoogleOsConfigGuestPolicies#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#delete GoogleOsConfigGuestPolicies#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#update GoogleOsConfigGuestPolicies#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9c8acac02b16ff4f3caa09591c4bc27f7175cf5311afc63307eb12501fbc06)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#create GoogleOsConfigGuestPolicies#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#delete GoogleOsConfigGuestPolicies#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_guest_policies#update GoogleOsConfigGuestPolicies#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigGuestPoliciesTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigGuestPoliciesTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigGuestPolicies.GoogleOsConfigGuestPoliciesTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97723053802bfc17ff7d41bc0e3fc990882397e385ee2d76c1222cf8da1ca09b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1af8f8a7e41b55bea6eeff77b3172ac0a812e712c12f524720c61e3f44130680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ebab584cde8094c2cd9ec4f4856abc5d65e07b81733503e67cadd0190910cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acce5c11cc666861b9e97e319501d3bbeaa4035f13066b590d90ad9035f7aaf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__490adec32b986c188bb071ca92599335b9c28897727414680adbad4f7953bc0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleOsConfigGuestPolicies",
    "GoogleOsConfigGuestPoliciesAssignment",
    "GoogleOsConfigGuestPoliciesAssignmentGroupLabels",
    "GoogleOsConfigGuestPoliciesAssignmentGroupLabelsList",
    "GoogleOsConfigGuestPoliciesAssignmentGroupLabelsOutputReference",
    "GoogleOsConfigGuestPoliciesAssignmentOsTypes",
    "GoogleOsConfigGuestPoliciesAssignmentOsTypesList",
    "GoogleOsConfigGuestPoliciesAssignmentOsTypesOutputReference",
    "GoogleOsConfigGuestPoliciesAssignmentOutputReference",
    "GoogleOsConfigGuestPoliciesConfig",
    "GoogleOsConfigGuestPoliciesPackageRepositories",
    "GoogleOsConfigGuestPoliciesPackageRepositoriesApt",
    "GoogleOsConfigGuestPoliciesPackageRepositoriesAptOutputReference",
    "GoogleOsConfigGuestPoliciesPackageRepositoriesGoo",
    "GoogleOsConfigGuestPoliciesPackageRepositoriesGooOutputReference",
    "GoogleOsConfigGuestPoliciesPackageRepositoriesList",
    "GoogleOsConfigGuestPoliciesPackageRepositoriesOutputReference",
    "GoogleOsConfigGuestPoliciesPackageRepositoriesYum",
    "GoogleOsConfigGuestPoliciesPackageRepositoriesYumOutputReference",
    "GoogleOsConfigGuestPoliciesPackageRepositoriesZypper",
    "GoogleOsConfigGuestPoliciesPackageRepositoriesZypperOutputReference",
    "GoogleOsConfigGuestPoliciesPackages",
    "GoogleOsConfigGuestPoliciesPackagesList",
    "GoogleOsConfigGuestPoliciesPackagesOutputReference",
    "GoogleOsConfigGuestPoliciesRecipes",
    "GoogleOsConfigGuestPoliciesRecipesArtifacts",
    "GoogleOsConfigGuestPoliciesRecipesArtifactsGcs",
    "GoogleOsConfigGuestPoliciesRecipesArtifactsGcsOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesArtifactsList",
    "GoogleOsConfigGuestPoliciesRecipesArtifactsOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesArtifactsRemote",
    "GoogleOsConfigGuestPoliciesRecipesArtifactsRemoteOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesInstallSteps",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtractionOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallationOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopyOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExecOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsList",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallationOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallationOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun",
    "GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRunOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesList",
    "GoogleOsConfigGuestPoliciesRecipesOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesUpdateSteps",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtractionOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallationOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopyOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExecOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsList",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallationOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallationOutputReference",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun",
    "GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRunOutputReference",
    "GoogleOsConfigGuestPoliciesTimeouts",
    "GoogleOsConfigGuestPoliciesTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ddba10db3e7f3246eac1da9216e7ca0ea76cbaa1cbd2b06f5e72fc5fa32a212c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    assignment: typing.Union[GoogleOsConfigGuestPoliciesAssignment, typing.Dict[builtins.str, typing.Any]],
    guest_policy_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    etag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    package_repositories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesPackageRepositories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesPackages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    recipes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesRecipes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__954c042769b419ec7e7785f15cfe4513494fc629169eede7e39240ef20d42b69(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__563735b7ed55992676c1ee272fbd631d1f1624df957ec761523bcc724ff0f5cf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesPackageRepositories, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363115a911ee9b470fcb3191c9c61b4d65a4eb7ddbf31f7fa8310429ec8bfbc9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesPackages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18286af7165ef3398d0dea8d5d2764cd328041b2fec44f0419432495ba8855be(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesRecipes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11fccfec326a6152512a4ba29491aef13e9843f8667369fc5ad08ad2e6180e27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0a9e002112132bfb849833582cdc25663930412c15f4b2ad2475f1cbead3dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e74439cc330239de01c61b2b75efad746b1dfd4fc2037e1c98d42490106ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a586de588b29177e75d543de67f4e96f351fdcc8c3055691d9f24fc6c8aa75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f00a00f2ca16db4407a9cca702b84db403e02ae872bd661f1f66da9607cdef9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1f1985c3d6b021c0c3c3af8d4708cf37be1adf2d1a9619e02118c27621b3b1(
    *,
    group_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesAssignmentGroupLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    os_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesAssignmentOsTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce28a2a09ebf824c0ee3e5faf2a12611e2ffa18103853fc104d59c6be060ea6(
    *,
    labels: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390e75c03430f1c7b1742681fae8eab0b00701855462b985a46f46f0143d86f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9d1186c9d685e0b972575d8f0802d94a35430521b36afb33c0baf82204b54c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f98c33897a781f477494ce2b90b91a0de2bf3310695e8701a8a717c842bbad7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1f99b1f1b87b91d830efd0fda61bf95f55a9a743dc6d2ff5994d38b4682834(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b744c49a89de0f6f3d23c9167c5d944947763c5036513b7d293654ebf78738f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66afbe395bc7dbe552b92282e4c4d460b5bfba8502e2dc8fbea623ab8a803777(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesAssignmentGroupLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0105a2e159ddc2d2dadfaae3c06e142c5bc463a00a9e91f2d7c0bd4d418c6093(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43f574170fed6a0ff5a307608222727ff0740a0ba71c8591dbb879cc59468f3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1c9103ee7b864a8bb0c09c25b001a9ed8b0068b7e1de9f66cbeae6d41397f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesAssignmentGroupLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb9662bc74c188498f24081a32f554e54897c8b226303830b5d930fca991a2e(
    *,
    os_architecture: typing.Optional[builtins.str] = None,
    os_short_name: typing.Optional[builtins.str] = None,
    os_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c334f79ae949b60ee6a6bb1ce42d8187b15305827e2aba0ffb973e91dfc8b2d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8adce14fcdd6c370d3b43d9136b7e3bf182078608077b086ffe2b01680bf671(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1d955ee3a93ad6f0b9cbf43d21e180acc67954aebe386ec46dcddf84f519ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db07ac8ca123c2795aef58e167b7fd6f57f3bb45240de542ea0b171cd3d56906(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1903394f51a63a37cc113bc63eed221c49611e0828d5669180d5af4e582779(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f33a72c6c4ef8bbbd5275ddbefc4a22095768671a1a6b65da417d7d0bf975189(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesAssignmentOsTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf13d5ec203c8cc8c0a32e28aa4d143162c54abdd8d9676c463181472bce6aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14bb08c61f28ea9b2e743414936f79d196c23044be964c97bce005d49f122c00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2677cfb6ee49f4c13cf2a3a0c1108e3b0c5e0742f03ede121c6f5da85d3b070(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43cb4570293e7379cce7f3d4037ba33928e242ce0cfd2ecff99ae0b04848959f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf7af63191723fbc77264416536d1f7d015a951bd3c4813d1345297f4a71454(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesAssignmentOsTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3880cc7f9e1054ab170c2cc8d6708414ffabc44238aecd1d707c2548bef81f5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55eca8116cc4925b94559de1ba5897f884e85a044fef648103f18b5d7db884b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesAssignmentGroupLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8956833d44d486c3183d4f09cf1370150aaa636710e03b7df3fadc86622a1ed9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesAssignmentOsTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a53e0862c28df666c7791d4605907065291b854f8ad4704929e73e5616861b6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2836348627a82eb743a42fda27ae5fc97a0c8a14b1994193dabc51fab9f39d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba38e7d2377cde5a930c34eb4a1d4b0720593225d1bbf2a580de5a5292bf0b6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85e025ac358ea93d1b7da08c2c6a54783acb2ade441aa122e5b5a668a489382(
    value: typing.Optional[GoogleOsConfigGuestPoliciesAssignment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24fce410ec029d89e7f4b2b42f6c1e6fedc785a033057c55df832041d71816de(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    assignment: typing.Union[GoogleOsConfigGuestPoliciesAssignment, typing.Dict[builtins.str, typing.Any]],
    guest_policy_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    etag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    package_repositories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesPackageRepositories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    packages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesPackages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    recipes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesRecipes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bcc07c6b4912d834e43d4241ec40a67716206c2327c8aacec034edc9c2b8c1c(
    *,
    apt: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesPackageRepositoriesApt, typing.Dict[builtins.str, typing.Any]]] = None,
    goo: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesPackageRepositoriesGoo, typing.Dict[builtins.str, typing.Any]]] = None,
    yum: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesPackageRepositoriesYum, typing.Dict[builtins.str, typing.Any]]] = None,
    zypper: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesPackageRepositoriesZypper, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531629a71ac016afd4b841f4a2200725d78dbb4c71a5354071710945d91e4ad1(
    *,
    components: typing.Sequence[builtins.str],
    distribution: builtins.str,
    uri: builtins.str,
    archive_type: typing.Optional[builtins.str] = None,
    gpg_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33ff132182b3833fcd84d52599e2d7ccc5656e3cebb9b5dbe047b627eea0a68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86841b5fc083090f66fd3ea04548c54b4db67dcbbb49b0b7b73f6a9b453fb96d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a543fc4d2fb380ec06ebc238d83b7d8422c0d8eb56822f89aad987c1a8a8d8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b507f1ac3a7d9ced4a9c44e3f242d9e0ca135bf1a827744cca41c15e1da1448e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f65d9e666a087c328463872dd3849b489fa9893d5436e1f7ef394bdec09f769(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a67954630ae7ecd1a3b047b6eeff0ba208d38ef74ab2146051f60ae83cdfb65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427d5ba88d69f473327d29351dcb72d73a03df9dcbfa25a20806b0a9deb774e2(
    value: typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesApt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3070d00cb5bcf5d8ef357d89c3010ef9c012292e58680a56ca5b44e8cdd5c699(
    *,
    name: builtins.str,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f2dda48c3533337dc9db590bec756bd7c951903de4c95c70c6aefe53b855f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c404e4cdafec3bec20dd10f946a62a37c360092580bf6ddccf33943e6f0c535(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74fdd1625db4b080f46b3bf1ca203e56d1817eb4bce71da2fc8a595844e96f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa82809b0bd950c7413e6e8dfc120836ce38af8d4deee11894bd94723d243e7(
    value: typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesGoo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd9dc63fb0a252f5d06dd1b5250d5cac2111faf4dcd0e93406a508e7f3692d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92150ccf23a8e94ed20e39af886ff167c47b89a2031086281e775a3774ea40d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f6bdd219fa8321787d26ec1025939509fa65ce45231124ed72fc2af99e38df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8de0d5db8d58c2fabaaf342098f74a368ef94f6a96f15a0ff25f2673dfbc30(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9bc1d6c72d4ac39240cdbeb02e518b97ee45765265251e5136ba65b250a7dd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3b75256cc9d1b83079eef01017048c0e8f5bb3f7050cdc155b5c6630871f9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesPackageRepositories]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b5f70f5564376f635a944bfa1d063858cfcf44ba123203ce29d119a18c6ce8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c498a4a8f089e29302dfe5e4d28a538bcbeb9711effa63dc2e5400373e69044(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesPackageRepositories]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8690ef411d08e20c6d06c2312fa68a77a384f2f90f747eea0e1d43c33441a0(
    *,
    base_url: builtins.str,
    id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e3322934016b821c0c57ec32089f0121032576b50ad825747824f84887c7bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9309461581e19e5effffa9843607eb2730accf75f70e5a9f92d217f76a730420(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4ad93ec5f1801408222579e77ce871c29687e837fc902bbea0679db0847b50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39780b0e61762a0bc4339e08a4b2c528e96c0cc5371a9ba1476a09af0b081f2a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b34d2b4781f312f21931e4c3a6daff2fab3c647246a0857d9f44924a9c94ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1589c5397c952998372d7ac09c4e208e631d474455527d8b842b2294e31de35d(
    value: typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesYum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6e5d715d2a9fb500e7481e36da1affaa6bd76d1c6e3459f1e81826574a0933(
    *,
    base_url: builtins.str,
    id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdfaa7b94f207df766a34156a264ac313d5a89a59ce0eace5626c2c10d86677c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1a04d4158a82d0dd3d34ecbdb5f5773d0ed8dc6e5c0e4ae330380bd417e19d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e498bb806ec2d327e5ead9f60559b453b3c6458185b051c3f77c2b9a70e0db1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854e7acb35ac6ce85467f622b56d7e6083285fcfb5857a1526b889ad7b7ecaf2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf6780af6ccca6dcd6a9e4c78efaded40082a60c6ffb3771131a0af9cf7d9cdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66272f314f1f0421174c5196b77759b35787137c4746ccb5864dddc141ed70b1(
    value: typing.Optional[GoogleOsConfigGuestPoliciesPackageRepositoriesZypper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c1eabfc420c9e6b8c855e2a08cc88f82f34bbbd34594fb687b1ef79dff7f9a(
    *,
    name: builtins.str,
    desired_state: typing.Optional[builtins.str] = None,
    manager: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904d9b08813cdc82227f50879e46b93341a0a2cbeb4fe4221e0e9740884d61f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52585d5bcaafd546037ac566871217a031c07b7490b6af6580fb97509c6b32d9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e5823903e9a99119e278973918433650ac646b88b3d035a9cdf4dced9661cfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca3dc7c677ff1fb0ccef675ddd5f0fbded3e018312eb77b0a491581618aa779(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9fb14a3386e668f2a60490222a75cef9c7b5352ff535c4953c1a3476646a5e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c359e1746a9ebc644492fd36546927e9412ca39da7a8a55c9793d36719ee533(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesPackages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891c314cd010230955cd6ef3991a1d1c743bc7904db2fd88f8f6c836afa59df6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3303efc10cf96cb596bee64d50447fc1dacf8636901d78f7ccf2099912811b77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca0f3e0ada631a516a8f73cf6c2d048efe23ce6a304ec6f5878dfe85f61cfab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f073495432a17d041294d3bb3912800c1ca544f566e7379db54b5c1e511ddb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a083ac1f8c8069e5e4b073ce05265c9083a5c12ddd9bab1d0c861faf02d7beb3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesPackages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ebf98f6b27dd77119a0053775a1c1e724fa5b1e073fd94e75d85c0b4e7b9be3(
    *,
    name: builtins.str,
    artifacts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesRecipesArtifacts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    desired_state: typing.Optional[builtins.str] = None,
    install_steps: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesRecipesInstallSteps, typing.Dict[builtins.str, typing.Any]]]]] = None,
    update_steps: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesRecipesUpdateSteps, typing.Dict[builtins.str, typing.Any]]]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5837409d979e19082b61d3b36b18ad1e2235c619d4af05a7583c519250fc834d(
    *,
    id: builtins.str,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesArtifactsGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    remote: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesArtifactsRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed4582fae3dd7d501b6927867166df6d8f4acb738a87d037e2bbcb38063f02a(
    *,
    bucket: typing.Optional[builtins.str] = None,
    generation: typing.Optional[jsii.Number] = None,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c37fec4105496c0d30b806fd74df267f36df421efcb2b4d6fdb409b2e2cdd85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb8fc601e0c1e535c8dc603e94bd481f2f96f5dc49136a80072f29f441b4d67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ade151bf3cb2f386fefda775dbabd958f303c0981cd4bf7de0c3bb8e8d6bdb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04b6a429aa46072f749ecf6d3cfd342ae331304ba59a5768d31e20b9102d95e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba1f254af275283f0776d56e607d0a67670db6d147231cf410d664d14919f1b(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesArtifactsGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb837e4c28cc7899fbb788b46c4dc1815881cd87d2137f025c9808de312ff503(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a79619db9841fdd78120a6608f48d44a989baa557589e7f45acc6be1eb8a59(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2240311a16bcb4353afde828daa9cf1927a85a64f42d69b05b4e2657a36a5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73cdee26391d0b109d9aafa23cd28baf9826b78f2a3b8a90ba495c4aefb6b197(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b452068caad0dd94b1cf5273383ba2c4d5a8018680bd88a1f863d5aec615cde7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d499d2c261dbdd500af4da94a42cc4dd2e1de078b9d0318eb16ac5613f2bf16e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesArtifacts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182066da260adf61f38318ad731ce8b6cef56a1bc8a8881b33323c84cc5360ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1252dfb29daa9a8e70bd2d864c2dd6227fbd5ed739947ef424c290b8c2123e98(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b6b37dc985f03c6ec56c653c20aff4a06a5a3c441aab5fc3057b008e21b19c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb799e113e88decf4541b4241651b064a0de962e92a1ce6e94d1758494355406(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipesArtifacts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c44ee9b9e65ef0f07af8d0d392c05b08bd3be49f803d7aaefa8bce3527ca0a(
    *,
    check_sum: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0547f6505ce7f409dc55cb95fdeabc86afb6de72ad216acc044ac4acf950fca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a075311f1b99469c09e5557a626afe46e8be9ccda8253db755647b801a1de20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d38be5b330d52a994b14f40ef627508c87f98e07f52c0fe61b4aacf68566ca1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f595e793df0c45a77dfeba93bcf69f76a9aac6f3d592e0f22b38536e0ca4191f(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesArtifactsRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d0ec2a66304470024f2638f2d7d728098c40aee50ae3bb1afa633f952fae8b(
    *,
    archive_extraction: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction, typing.Dict[builtins.str, typing.Any]]] = None,
    dpkg_installation: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation, typing.Dict[builtins.str, typing.Any]]] = None,
    file_copy: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy, typing.Dict[builtins.str, typing.Any]]] = None,
    file_exec: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec, typing.Dict[builtins.str, typing.Any]]] = None,
    msi_installation: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation, typing.Dict[builtins.str, typing.Any]]] = None,
    rpm_installation: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation, typing.Dict[builtins.str, typing.Any]]] = None,
    script_run: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ca3cd58b8731976c4d5f2e13907ce8afbf335bc3a1eb6933ff3095a5a32be7(
    *,
    artifact_id: builtins.str,
    type: builtins.str,
    destination: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47acd88987442dfcc94191deff663833b219052d96bd83d2c9e76a033fee60fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__454069613145940f3762d791da8f6a6645a816c7b582e7eca9e3f9a5bbcf28bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6177dad4f43dc7a35401cfab0500bce8396599adcf5058a58864530c692acf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70fd23136f1a8ce72b093de97a1d90d6e687470531d01f477d5c238574d36ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39288e6b29d8968b5dd24f5a5522a020234cf2b2e974d95a59c05b67d284a3b2(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsArchiveExtraction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8930b3fb3ab2d5481c0ba8afc67e0c823b7e4e62b9ec0916a097a8580343c544(
    *,
    artifact_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5dd591284c4cd1d0e5c0d32496ac6273c345c8e1819c1fa52a12ff9f21b65f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e362f9c047b27c709b6ec46dd5202f9c0178ceb37fe4b4598e2b3cf798ea9845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13303b027026e51736c59fafd7c5fab268c2847e10f73f0f737ebc8063f505f5(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsDpkgInstallation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316217a9fb30acdd86db1a8c16184dc6c1efd212398444798f2773613359c6b2(
    *,
    artifact_id: builtins.str,
    destination: builtins.str,
    overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    permissions: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b6f887d82c99087d88180e9bdc77046b4b6dcfc4fe8ef89aa53bb9dfb99748(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd46b1d1d16d04896fff552e646114477cc42e58eb7fe14751e895a1af0edf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e9a01ca2a79256e117e9c0f543c022135e930eb9dc41ce00237b9c086c4036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a523da96f08eb0c7f2a796bf5c0aa58a950776f503ed79bf82721612761a3eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394abc0e0d85fc181db8840c4324c86a3060e36ac0af0592d5bbe222a26f03b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1623a32248b5b051ef881ae35f38151fb068502bdddb28b2eb3e2ffd1917c9bc(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileCopy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45fee08a7291146b25c9841b2ec1e7d1554e013f69b09fb5f4a151d782e194c2(
    *,
    allowed_exit_codes: typing.Optional[builtins.str] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    artifact_id: typing.Optional[builtins.str] = None,
    local_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e36c2fbed3589dda5a1a7db12bc796edb3b234a04fcd0b28913fc81e47e206(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1329ba825bb8b0137869256e1a8a167e405a969be0fb322ee1a370f380e1326b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda44815b858fb583d239b82b6bfd29e950b39532defe706d35c18087cb13dd2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c978a4e6dce888058fae4e81f58139c5be49d77f55b460a655d2c8af0bdbce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e00ecbf9a0a3375293e94f7094cf5613f9ba9155144b91773ab59032cbbf073(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4831a806ee62a13d2fec9df7f0a3be720c77c2b37d18a4e912e04b0ce3ad35a0(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsFileExec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90202a6642609e296db6b6347ad268ac8d1c7271599cf859a062a0be92126e13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9b8aa66541bacb5c2b3014664269819c0c31cb61d4d12e4ccf1fc98d452fbb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b2f2a398efa8c81d22ec59ea18ce96cb5c8fab02b5d3a3a501f8a3ee8e7120(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c33d429316ac18353d1bfa1568909bf6357187cc33c64ee442981e576a6ffbd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abec21655d6a3ee9adc5c90e38a4431eff57278fe3ea5f91f67b82d65593fde3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ceb5f9ea1362b9aafbc5be9515021b1bb5e72217577506bfe4840590116279(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesInstallSteps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ac16d069e0c7f5e5292dba57b67f2e600060bc5712a98944ad51c3f9d3f43f(
    *,
    artifact_id: builtins.str,
    allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    flags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2792d383245c76e0095c58e791346eb1cccaa712b89d4dfba8523b5d404df9af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814b03b35eebdbeb6bf4fa69e5be4f9479ae9fc20277b0460e10107490ac0b2c(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865b534b9fa7b60fe015cb4e01abe1c97ce45a164f476beb2bb5575ee2ae007c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50bf95c9851f23379f2adf38d0ce210c5b0e6686e12722075329c2f3c0eca29d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0cfbc5218e14e779917ff05f90fc99b49e419f5c10783b727c15b79a9a25e1(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsMsiInstallation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c8930bdb87751a14d527cbfe1faf0dfb59583b193250cc50d01d2d993fac13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48142a1d25aa837cb4cbfa399fdc16e4dfd8100b954b03ac881789722fb1708c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipesInstallSteps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56938619bd8dfe48d15a232f9cfed71e7db767c5a50ed05fbe9ac4a34bd26fd(
    *,
    artifact_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbac15be9f0c32ade9ffada18947ae3daeb2a5efa89c4cf5893a12580c5fea42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e8b491c0c81ccfb0418773266bc95baee7357310364711db91c7726e33c0f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c40018c0f36d2ee32f891c0f1352ba63a881719dba88b64acd1bcc0f0251175(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsRpmInstallation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a702921d59ee78169e401e97fec34d150d7f0c2012956bc8f7a115101a4c835f(
    *,
    script: builtins.str,
    allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    interpreter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d048cde5518a2c86da144318357d50c5d84cfdbb4634ea39d9bcec483297374(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87c77cef6b50735b1f45f57130b5af00e8d1d56e5504822077278fb509dff9c(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ba25a4e3729026caa750888c54a1f053b795cb7cd925ce4affedc0d0b3eda7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54660dec1cc29e9e55e3c1418be2c2b4c750375d103238602ff1a42f66eb79f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e5e8a545848c85798a2d42e91b626d8cdd17022b072b7c674d97e86b77a716(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesInstallStepsScriptRun],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ea35f3a8d8301247e8f84f5f5e10ac7aeef3449f38d70a3ec62d7fb447b8e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f292a02d2fcc5f3b93dbf65c1e1d5a1d24c70f8f02ed7cd5fac1fc54aecb69(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983b15e869ffe2f1e092eebb0b8448abbbfdc2e925a3385857439e20c4e38b1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79352c878149b3902405493326d71403b6b2f1d910b7809639cd12460fc48395(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8fda1d4ed4b354a3ec54bb7d0c933f1ffdcb45f8aec25ffd04c300744d8b319(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c05548bb1af2eeebf8f739575fc91c0b6028542910ff74757dba4746c7c1e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d10e8595f6d417b1c8b86005cfcd1985b31c0c930fd0b7ef84802f090729521(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d7d28c6691e109626b46c667989816e90be5605ec80b272c2d451e612445c7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesRecipesArtifacts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f9e7ddecdf30fef8dae40af2cc38ab564d22e83a223a00127c65741f015e14(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesRecipesInstallSteps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cec13c6a7f3e818ac0704dd604fb1d3eb590edfb22619e990072aceecb9c137(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigGuestPoliciesRecipesUpdateSteps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c82f8d9d4390004059633f28fb3b34ff73ba72bc3f8e383316bb5439bc92de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77460f8ad86afec7ede7ccac4bcfa0b7e9dd212b158f64403aa97110120582e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc869115cbf2694425b7099c114caeab78d17f5bc10b33a231329a17f04ed953(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643875c8a78be33983c4a76de8c8ab4e83bf34f6e55aa2396529ac87e8a27262(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef10b2c8ce8b11ddfe3bb3aa235a5442ba8d18409da9553443bce2d04001e0d0(
    *,
    archive_extraction: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction, typing.Dict[builtins.str, typing.Any]]] = None,
    dpkg_installation: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation, typing.Dict[builtins.str, typing.Any]]] = None,
    file_copy: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy, typing.Dict[builtins.str, typing.Any]]] = None,
    file_exec: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec, typing.Dict[builtins.str, typing.Any]]] = None,
    msi_installation: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation, typing.Dict[builtins.str, typing.Any]]] = None,
    rpm_installation: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation, typing.Dict[builtins.str, typing.Any]]] = None,
    script_run: typing.Optional[typing.Union[GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11170ff88e4945521d1431a1cf4bb2e23468cb6cabb00e9c8388032d3630a4b4(
    *,
    artifact_id: builtins.str,
    type: builtins.str,
    destination: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc39e1bde116761569964a814b49e7f9a205cfa31bb726afccfc2fdbf984301a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d4ea8fab62496ae765e56c2c421d6494d53d005dea5bd2f2de1e614a4c43545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df5535da7b703d0d78d841ece92c3c919666b066e6aa692028a802759f58d22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b09528a968f292ea243f756a83be48c44d5b6ca2bd002dcce36a8fff67b3de3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12bc3d501247ca017ec3ca1e575d7be083f16a107b7c9337dab737d052b2814b(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsArchiveExtraction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f62c5cf8da5ed10a27f2198c3e8e8fb613edcb329ffe3f27c4e68531bdf2ef(
    *,
    artifact_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada181a7340e297108ced84e7df57a2058e7c4b93b3c8830b24e4bafacafd406(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ad70ef4cbf333d81c32e0a0380e56b46d746848b142f2d1fbed0e525a9527e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea083ac3b99f23ad4c5bd58c48ce29427ad08c3bd6e44f1fc4b14d0f2e63a66(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsDpkgInstallation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41080f970bb0586136d39018036a212139c2fb6f755fbe1b1a64dbb60a14749(
    *,
    artifact_id: builtins.str,
    destination: builtins.str,
    overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    permissions: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2101fc6d94101344e823912783fdd82299e6dca3bfa33a762931bc28c566cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068680c35cd5f0df22baf02ff2a43dbb045da5ff6f80e251067315eb9682cd56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944b6ae823e89210376f34d81221aad582578d8fd384307eb811283f935457e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42218a013a78163a99376e411bd1a0c26bc0f15fbb048b319e48db5b451d407e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c928e10a445f338c33ec130dd0bc7440d7ef7dcfae63171f95346385c00e51b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d52df47cea2578cda2874084a1689d4ef3b74112e51c6163ed4cbfe664a79b5(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileCopy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb00599a8cf774220ad1ceedd94bf53097349c407508c22b933f470a124913b3(
    *,
    allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    artifact_id: typing.Optional[builtins.str] = None,
    local_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe6764ec540c345fd3d271daabf25b7f8845c9fa09e2ea4d5e7c96389175067(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073b07736facc964e564702ff6bfdcf2f79fe7532f77eda6a7cbc6440771b1a1(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6e35af1dbc3e6c6983e9e1158f9ec9bb5f547f5af694fcbf4b058e81768287(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910d951a1ce6e5a1400254d26910e9401720fe30caa91ad4fbbd0a7101918c1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1ae2009f3f0830d058a944de98f9570bbf34f0464cdfb6eae75ac652288ff2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ff4ba25abe97386543b2a105e258e6097e9166fc2bd853447d4226f602710c(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsFileExec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d701cad627087c3a80f44531fb6082ccbd3c918d8c2ffd204f43b547b68dfa58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95159a1607491ae73316e105db406e4dcd3e06405740353abc0968f7487787e6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4e5ca04b1d240889eabc0de859b11758d38920edb87d4eb676ad55994adf4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6054c8b0100d59c87a3ec43aa01cdceeef54eba2865bc588302d2fed6f45fab2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d53db2c3630fa47ba66ce21aa19c69e6802cf46c8db4aa5e7076ee3e7b10f04(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f17ec533d71766f8313928166d08bdcb2259a179fed1359fdbbc6a83c8b7f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigGuestPoliciesRecipesUpdateSteps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6404aa47814caef1830b9b61f76210ad5d26cd68c452b711451537acd7ced9(
    *,
    artifact_id: builtins.str,
    allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    flags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e9f4b8ec61e36421c8de28d04cd11edf7bfc34825ac45f7fec0d3a2f40fd1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7207a3d7196975bc47d2cdb6af7d222b46e880908189a0066125c5192a70b76(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11075d44291f50f881149bfa69d061ac26c0aa728c0ab19e85e60779d901a61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691c38303729396ea455d2a1ebc7770e3d5db59cc68abec39fad65e3c6350d59(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c8c20fb88a2d10cebae9c0aaeb94afe2a7d8e4fa2a2e6a9f1585d8014aada2(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsMsiInstallation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20976fa817e4e19cbbc012f49f13e37e148e4a9318e812684a11f7ff87702c74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c80be6f9bc726251f22aa525e0f51e5e849f70f665aa5c81ba134098e67cb1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesRecipesUpdateSteps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc08a3fce2d4bf4f009102a1dd39210ae263a3b26298a6cb3a1c7f62ec668fea(
    *,
    artifact_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606b329f2d003aea77b3e777d01ddb55276adb86d62079b4662d948cd34cbedb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0776ee96fbc36b63974b2152434dfc11f33ede5b94d7466d2fda03242fb2a3b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf73d7a044bf1f8574258654e3700e887dfe4384bc40f875de745881105a9925(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsRpmInstallation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9871f623430f667bb61b9c9a7f42711cf2a40d3c4eed2f3323b11579d001a4(
    *,
    script: builtins.str,
    allowed_exit_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    interpreter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd3b3aa93281118b9037aca58d653ab2b7f4ee71a727c224c83e21e2cd2db40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378f7fb38c35d49710496bdc10d6b2a61e22adccd6f7cb56abafb132077ef7df(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af948c4b3ca58d56a9bda1e92442279b5dfc8128954d16d8817e87ee74a7fb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fc7a5ab42993561129d2e5e211e25ffc26327e81a88b4cc8dcbefa9cd92370(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db6a25d0eeb29c10fbc171c476d01b96995a7e85837fafc85fa2528ba842de4(
    value: typing.Optional[GoogleOsConfigGuestPoliciesRecipesUpdateStepsScriptRun],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9c8acac02b16ff4f3caa09591c4bc27f7175cf5311afc63307eb12501fbc06(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97723053802bfc17ff7d41bc0e3fc990882397e385ee2d76c1222cf8da1ca09b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af8f8a7e41b55bea6eeff77b3172ac0a812e712c12f524720c61e3f44130680(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ebab584cde8094c2cd9ec4f4856abc5d65e07b81733503e67cadd0190910cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acce5c11cc666861b9e97e319501d3bbeaa4035f13066b590d90ad9035f7aaf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490adec32b986c188bb071ca92599335b9c28897727414680adbad4f7953bc0d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigGuestPoliciesTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
