r'''
# `google_gke_hub_scope_rbac_role_binding`

Refer to the Terraform Registry for docs: [`google_gke_hub_scope_rbac_role_binding`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding).
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


class GkeHubScopeRbacRoleBinding(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubScopeRbacRoleBinding.GkeHubScopeRbacRoleBinding",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding google_gke_hub_scope_rbac_role_binding}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        role: typing.Union["GkeHubScopeRbacRoleBindingRole", typing.Dict[builtins.str, typing.Any]],
        scope_id: builtins.str,
        scope_rbac_role_binding_id: builtins.str,
        group: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeHubScopeRbacRoleBindingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding google_gke_hub_scope_rbac_role_binding} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param role: role block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#role GkeHubScopeRbacRoleBinding#role}
        :param scope_id: Id of the scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#scope_id GkeHubScopeRbacRoleBinding#scope_id}
        :param scope_rbac_role_binding_id: The client-provided identifier of the RBAC Role Binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#scope_rbac_role_binding_id GkeHubScopeRbacRoleBinding#scope_rbac_role_binding_id}
        :param group: Principal that is be authorized in the cluster (at least of one the oneof is required). Updating one will unset the other automatically. group is the group, as seen by the kubernetes cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#group GkeHubScopeRbacRoleBinding#group}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#id GkeHubScopeRbacRoleBinding#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels for this ScopeRBACRoleBinding. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#labels GkeHubScopeRbacRoleBinding#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#project GkeHubScopeRbacRoleBinding#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#timeouts GkeHubScopeRbacRoleBinding#timeouts}
        :param user: Principal that is be authorized in the cluster (at least of one the oneof is required). Updating one will unset the other automatically. user is the name of the user as seen by the kubernetes cluster, example "alice" or "alice@domain.tld" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#user GkeHubScopeRbacRoleBinding#user}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5d9a726027ca44c13f03c016d5d160aed30eac1ee4ffbd9c3bc8789ff8ac71)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GkeHubScopeRbacRoleBindingConfig(
            role=role,
            scope_id=scope_id,
            scope_rbac_role_binding_id=scope_rbac_role_binding_id,
            group=group,
            id=id,
            labels=labels,
            project=project,
            timeouts=timeouts,
            user=user,
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
        '''Generates CDKTF code for importing a GkeHubScopeRbacRoleBinding resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeHubScopeRbacRoleBinding to import.
        :param import_from_id: The id of the existing GkeHubScopeRbacRoleBinding that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeHubScopeRbacRoleBinding to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__039dd90c540a110ecd531666680055d20025dfc0d5bedf0562436ef5387d2504)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRole")
    def put_role(
        self,
        *,
        custom_role: typing.Optional[builtins.str] = None,
        predefined_role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_role: CustomRole is the custom Kubernetes ClusterRole to be used. The custom role format must be allowlisted in the rbacrolebindingactuation feature and RFC 1123 compliant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#custom_role GkeHubScopeRbacRoleBinding#custom_role}
        :param predefined_role: PredefinedRole is an ENUM representation of the default Kubernetes Roles Possible values: ["UNKNOWN", "ADMIN", "EDIT", "VIEW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#predefined_role GkeHubScopeRbacRoleBinding#predefined_role}
        '''
        value = GkeHubScopeRbacRoleBindingRole(
            custom_role=custom_role, predefined_role=predefined_role
        )

        return typing.cast(None, jsii.invoke(self, "putRole", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#create GkeHubScopeRbacRoleBinding#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#delete GkeHubScopeRbacRoleBinding#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#update GkeHubScopeRbacRoleBinding#update}.
        '''
        value = GkeHubScopeRbacRoleBindingTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetGroup")
    def reset_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroup", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

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
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> "GkeHubScopeRbacRoleBindingRoleOutputReference":
        return typing.cast("GkeHubScopeRbacRoleBindingRoleOutputReference", jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> "GkeHubScopeRbacRoleBindingStateList":
        return typing.cast("GkeHubScopeRbacRoleBindingStateList", jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GkeHubScopeRbacRoleBindingTimeoutsOutputReference":
        return typing.cast("GkeHubScopeRbacRoleBindingTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional["GkeHubScopeRbacRoleBindingRole"]:
        return typing.cast(typing.Optional["GkeHubScopeRbacRoleBindingRole"], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeRbacRoleBindingIdInput")
    def scope_rbac_role_binding_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeRbacRoleBindingIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeHubScopeRbacRoleBindingTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeHubScopeRbacRoleBindingTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0f4edfa3168120c3a75e390b0ade7bb26ba6111bfe86376b6086680631e30fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377b1c3ef96721a30217a87bcd34e280fb51543700d958cf924fe7e5b289138e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f535d270e3673ae86c04303704fdffb0885cd5267ff677e4f1fe341a2eacef6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa0ff30d520c4ad515b96702cdf9b07d24fc12f346adcf22b58a995d0eacb81b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a724b01c8aa442b53412a3d7f4c83c47943bc8ff6787b3330c3dd87ea47a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopeRbacRoleBindingId")
    def scope_rbac_role_binding_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeRbacRoleBindingId"))

    @scope_rbac_role_binding_id.setter
    def scope_rbac_role_binding_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aaa602dd42bc289aebd71a3cb8fc8a682fa136a76c3d7e66964fc49cd3e5910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeRbacRoleBindingId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5316a2516f750b75595b885de0f209ad016f214c84acb121f4abdb7862e64a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubScopeRbacRoleBinding.GkeHubScopeRbacRoleBindingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "role": "role",
        "scope_id": "scopeId",
        "scope_rbac_role_binding_id": "scopeRbacRoleBindingId",
        "group": "group",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
        "user": "user",
    },
)
class GkeHubScopeRbacRoleBindingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        role: typing.Union["GkeHubScopeRbacRoleBindingRole", typing.Dict[builtins.str, typing.Any]],
        scope_id: builtins.str,
        scope_rbac_role_binding_id: builtins.str,
        group: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeHubScopeRbacRoleBindingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param role: role block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#role GkeHubScopeRbacRoleBinding#role}
        :param scope_id: Id of the scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#scope_id GkeHubScopeRbacRoleBinding#scope_id}
        :param scope_rbac_role_binding_id: The client-provided identifier of the RBAC Role Binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#scope_rbac_role_binding_id GkeHubScopeRbacRoleBinding#scope_rbac_role_binding_id}
        :param group: Principal that is be authorized in the cluster (at least of one the oneof is required). Updating one will unset the other automatically. group is the group, as seen by the kubernetes cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#group GkeHubScopeRbacRoleBinding#group}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#id GkeHubScopeRbacRoleBinding#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels for this ScopeRBACRoleBinding. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#labels GkeHubScopeRbacRoleBinding#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#project GkeHubScopeRbacRoleBinding#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#timeouts GkeHubScopeRbacRoleBinding#timeouts}
        :param user: Principal that is be authorized in the cluster (at least of one the oneof is required). Updating one will unset the other automatically. user is the name of the user as seen by the kubernetes cluster, example "alice" or "alice@domain.tld" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#user GkeHubScopeRbacRoleBinding#user}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(role, dict):
            role = GkeHubScopeRbacRoleBindingRole(**role)
        if isinstance(timeouts, dict):
            timeouts = GkeHubScopeRbacRoleBindingTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36413bc59b81e009d35f23109d5b24144b5d046c0003141a39a39fba9cb0ab9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument scope_id", value=scope_id, expected_type=type_hints["scope_id"])
            check_type(argname="argument scope_rbac_role_binding_id", value=scope_rbac_role_binding_id, expected_type=type_hints["scope_rbac_role_binding_id"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role": role,
            "scope_id": scope_id,
            "scope_rbac_role_binding_id": scope_rbac_role_binding_id,
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
        if group is not None:
            self._values["group"] = group
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user is not None:
            self._values["user"] = user

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
    def role(self) -> "GkeHubScopeRbacRoleBindingRole":
        '''role block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#role GkeHubScopeRbacRoleBinding#role}
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast("GkeHubScopeRbacRoleBindingRole", result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''Id of the scope.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#scope_id GkeHubScopeRbacRoleBinding#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope_rbac_role_binding_id(self) -> builtins.str:
        '''The client-provided identifier of the RBAC Role Binding.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#scope_rbac_role_binding_id GkeHubScopeRbacRoleBinding#scope_rbac_role_binding_id}
        '''
        result = self._values.get("scope_rbac_role_binding_id")
        assert result is not None, "Required property 'scope_rbac_role_binding_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''Principal that is be authorized in the cluster (at least of one the oneof is required).

        Updating one will unset the other automatically.
        group is the group, as seen by the kubernetes cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#group GkeHubScopeRbacRoleBinding#group}
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#id GkeHubScopeRbacRoleBinding#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels for this ScopeRBACRoleBinding.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#labels GkeHubScopeRbacRoleBinding#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#project GkeHubScopeRbacRoleBinding#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeHubScopeRbacRoleBindingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#timeouts GkeHubScopeRbacRoleBinding#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeHubScopeRbacRoleBindingTimeouts"], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''Principal that is be authorized in the cluster (at least of one the oneof is required).

        Updating one will unset the other automatically.
        user is the name of the user as seen by the kubernetes cluster, example
        "alice" or "alice@domain.tld"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#user GkeHubScopeRbacRoleBinding#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubScopeRbacRoleBindingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubScopeRbacRoleBinding.GkeHubScopeRbacRoleBindingRole",
    jsii_struct_bases=[],
    name_mapping={"custom_role": "customRole", "predefined_role": "predefinedRole"},
)
class GkeHubScopeRbacRoleBindingRole:
    def __init__(
        self,
        *,
        custom_role: typing.Optional[builtins.str] = None,
        predefined_role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_role: CustomRole is the custom Kubernetes ClusterRole to be used. The custom role format must be allowlisted in the rbacrolebindingactuation feature and RFC 1123 compliant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#custom_role GkeHubScopeRbacRoleBinding#custom_role}
        :param predefined_role: PredefinedRole is an ENUM representation of the default Kubernetes Roles Possible values: ["UNKNOWN", "ADMIN", "EDIT", "VIEW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#predefined_role GkeHubScopeRbacRoleBinding#predefined_role}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d477b50cde4a1527e2138126c81f4a6cc72b83e07f967c2126d0e8fb78873fd6)
            check_type(argname="argument custom_role", value=custom_role, expected_type=type_hints["custom_role"])
            check_type(argname="argument predefined_role", value=predefined_role, expected_type=type_hints["predefined_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_role is not None:
            self._values["custom_role"] = custom_role
        if predefined_role is not None:
            self._values["predefined_role"] = predefined_role

    @builtins.property
    def custom_role(self) -> typing.Optional[builtins.str]:
        '''CustomRole is the custom Kubernetes ClusterRole to be used.

        The custom role format must be allowlisted in the rbacrolebindingactuation feature and RFC 1123 compliant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#custom_role GkeHubScopeRbacRoleBinding#custom_role}
        '''
        result = self._values.get("custom_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def predefined_role(self) -> typing.Optional[builtins.str]:
        '''PredefinedRole is an ENUM representation of the default Kubernetes Roles Possible values: ["UNKNOWN", "ADMIN", "EDIT", "VIEW"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#predefined_role GkeHubScopeRbacRoleBinding#predefined_role}
        '''
        result = self._values.get("predefined_role")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubScopeRbacRoleBindingRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubScopeRbacRoleBindingRoleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubScopeRbacRoleBinding.GkeHubScopeRbacRoleBindingRoleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5d599d16bb40612112bcbea400126299e72986a2f88c07aee1e3faf03fb0b71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomRole")
    def reset_custom_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRole", []))

    @jsii.member(jsii_name="resetPredefinedRole")
    def reset_predefined_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredefinedRole", []))

    @builtins.property
    @jsii.member(jsii_name="customRoleInput")
    def custom_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="predefinedRoleInput")
    def predefined_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "predefinedRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="customRole")
    def custom_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customRole"))

    @custom_role.setter
    def custom_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585945e93f79aceff6bddf00727d10029e046f75c77afc437cf4baed60b0b216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="predefinedRole")
    def predefined_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "predefinedRole"))

    @predefined_role.setter
    def predefined_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d90ed7d2ff9897561b2f46fc907a460f9ed89e4f0f6ee6deae726130452cba01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predefinedRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubScopeRbacRoleBindingRole]:
        return typing.cast(typing.Optional[GkeHubScopeRbacRoleBindingRole], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubScopeRbacRoleBindingRole],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af1de854ce82aee05168f08309cffe83066486607fe9f46a2d4a77b9b4599d2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubScopeRbacRoleBinding.GkeHubScopeRbacRoleBindingState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeHubScopeRbacRoleBindingState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubScopeRbacRoleBindingState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubScopeRbacRoleBindingStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubScopeRbacRoleBinding.GkeHubScopeRbacRoleBindingStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acaa55b07ac3e491bf9445a522011683d8e11030be412e0852ceb515463ed25b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeHubScopeRbacRoleBindingStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef43c0ba39dcd87178d17e9cdd34ddd95b8ab802e27f2806103eed26f66ba337)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubScopeRbacRoleBindingStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3fad9fc412d755268c2203b372a9c442f5e3df7486e201e65d645ee47cba14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b203eaefefc4e0e8231871c8ac6fc42f7087e310c57717ca5363b42159eeb7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b90e756f97f1a4d50039e18c72bc5036e85083626f45a73efc00eba0f44442a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeHubScopeRbacRoleBindingStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubScopeRbacRoleBinding.GkeHubScopeRbacRoleBindingStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbd81af50f2fc9ad0e5de0cd2aae6b741d8b2c38904da57615eba8e21f76472a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubScopeRbacRoleBindingState]:
        return typing.cast(typing.Optional[GkeHubScopeRbacRoleBindingState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubScopeRbacRoleBindingState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39baa39b1ed801efdfe3763018c74fef8b562f58eac315af7e439bf33ac0b286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubScopeRbacRoleBinding.GkeHubScopeRbacRoleBindingTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeHubScopeRbacRoleBindingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#create GkeHubScopeRbacRoleBinding#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#delete GkeHubScopeRbacRoleBinding#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#update GkeHubScopeRbacRoleBinding#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7364a94d76eeb343e0493606c20485d8536ba8773a588db2a97b6092131219)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#create GkeHubScopeRbacRoleBinding#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#delete GkeHubScopeRbacRoleBinding#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_scope_rbac_role_binding#update GkeHubScopeRbacRoleBinding#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubScopeRbacRoleBindingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubScopeRbacRoleBindingTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubScopeRbacRoleBinding.GkeHubScopeRbacRoleBindingTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f503fd6a301a9c13d00c65671d7cddf2bfb9ced09d2b48938c4bf53e8f3302e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d12afce96879c897a915c5c604bbdae78cdb355f4e43d1ce523258c425c0961d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6efcafc84522c795a4aaae0b604da01ddfc9257dd8f5122cc3fca506e7a398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0133dd629cbab42c544cdaadb9d6266f86b3afd035afc401f6460152cd232c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubScopeRbacRoleBindingTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubScopeRbacRoleBindingTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubScopeRbacRoleBindingTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347c2e5f68aad370966a1842131ef573d07b33c4d038ba97462246e81b9cd1d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GkeHubScopeRbacRoleBinding",
    "GkeHubScopeRbacRoleBindingConfig",
    "GkeHubScopeRbacRoleBindingRole",
    "GkeHubScopeRbacRoleBindingRoleOutputReference",
    "GkeHubScopeRbacRoleBindingState",
    "GkeHubScopeRbacRoleBindingStateList",
    "GkeHubScopeRbacRoleBindingStateOutputReference",
    "GkeHubScopeRbacRoleBindingTimeouts",
    "GkeHubScopeRbacRoleBindingTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2a5d9a726027ca44c13f03c016d5d160aed30eac1ee4ffbd9c3bc8789ff8ac71(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    role: typing.Union[GkeHubScopeRbacRoleBindingRole, typing.Dict[builtins.str, typing.Any]],
    scope_id: builtins.str,
    scope_rbac_role_binding_id: builtins.str,
    group: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeHubScopeRbacRoleBindingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__039dd90c540a110ecd531666680055d20025dfc0d5bedf0562436ef5387d2504(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f4edfa3168120c3a75e390b0ade7bb26ba6111bfe86376b6086680631e30fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377b1c3ef96721a30217a87bcd34e280fb51543700d958cf924fe7e5b289138e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f535d270e3673ae86c04303704fdffb0885cd5267ff677e4f1fe341a2eacef6c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0ff30d520c4ad515b96702cdf9b07d24fc12f346adcf22b58a995d0eacb81b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a724b01c8aa442b53412a3d7f4c83c47943bc8ff6787b3330c3dd87ea47a96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aaa602dd42bc289aebd71a3cb8fc8a682fa136a76c3d7e66964fc49cd3e5910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5316a2516f750b75595b885de0f209ad016f214c84acb121f4abdb7862e64a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36413bc59b81e009d35f23109d5b24144b5d046c0003141a39a39fba9cb0ab9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    role: typing.Union[GkeHubScopeRbacRoleBindingRole, typing.Dict[builtins.str, typing.Any]],
    scope_id: builtins.str,
    scope_rbac_role_binding_id: builtins.str,
    group: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeHubScopeRbacRoleBindingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d477b50cde4a1527e2138126c81f4a6cc72b83e07f967c2126d0e8fb78873fd6(
    *,
    custom_role: typing.Optional[builtins.str] = None,
    predefined_role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d599d16bb40612112bcbea400126299e72986a2f88c07aee1e3faf03fb0b71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585945e93f79aceff6bddf00727d10029e046f75c77afc437cf4baed60b0b216(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90ed7d2ff9897561b2f46fc907a460f9ed89e4f0f6ee6deae726130452cba01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1de854ce82aee05168f08309cffe83066486607fe9f46a2d4a77b9b4599d2a(
    value: typing.Optional[GkeHubScopeRbacRoleBindingRole],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acaa55b07ac3e491bf9445a522011683d8e11030be412e0852ceb515463ed25b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef43c0ba39dcd87178d17e9cdd34ddd95b8ab802e27f2806103eed26f66ba337(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3fad9fc412d755268c2203b372a9c442f5e3df7486e201e65d645ee47cba14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b203eaefefc4e0e8231871c8ac6fc42f7087e310c57717ca5363b42159eeb7f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90e756f97f1a4d50039e18c72bc5036e85083626f45a73efc00eba0f44442a5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd81af50f2fc9ad0e5de0cd2aae6b741d8b2c38904da57615eba8e21f76472a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39baa39b1ed801efdfe3763018c74fef8b562f58eac315af7e439bf33ac0b286(
    value: typing.Optional[GkeHubScopeRbacRoleBindingState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7364a94d76eeb343e0493606c20485d8536ba8773a588db2a97b6092131219(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f503fd6a301a9c13d00c65671d7cddf2bfb9ced09d2b48938c4bf53e8f3302e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12afce96879c897a915c5c604bbdae78cdb355f4e43d1ce523258c425c0961d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6efcafc84522c795a4aaae0b604da01ddfc9257dd8f5122cc3fca506e7a398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0133dd629cbab42c544cdaadb9d6266f86b3afd035afc401f6460152cd232c83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347c2e5f68aad370966a1842131ef573d07b33c4d038ba97462246e81b9cd1d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubScopeRbacRoleBindingTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
