r'''
# `google_cloud_identity_group_membership`

Refer to the Terraform Registry for docs: [`google_cloud_identity_group_membership`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership).
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


class GoogleCloudIdentityGroupMembership(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudIdentityGroupMembership.GoogleCloudIdentityGroupMembership",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership google_cloud_identity_group_membership}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        group: builtins.str,
        roles: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudIdentityGroupMembershipRoles", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        member_key: typing.Optional[typing.Union["GoogleCloudIdentityGroupMembershipMemberKey", typing.Dict[builtins.str, typing.Any]]] = None,
        preferred_member_key: typing.Optional[typing.Union["GoogleCloudIdentityGroupMembershipPreferredMemberKey", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudIdentityGroupMembershipTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership google_cloud_identity_group_membership} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param group: The name of the Group to create this membership in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#group GoogleCloudIdentityGroupMembership#group}
        :param roles: roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#roles GoogleCloudIdentityGroupMembership#roles}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#id GoogleCloudIdentityGroupMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param member_key: member_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#member_key GoogleCloudIdentityGroupMembership#member_key}
        :param preferred_member_key: preferred_member_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#preferred_member_key GoogleCloudIdentityGroupMembership#preferred_member_key}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#timeouts GoogleCloudIdentityGroupMembership#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8940681f98a3eeb6dc87a4554a6a09babf451bb3d3b2fb2879ed621d79ac2d8a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCloudIdentityGroupMembershipConfig(
            group=group,
            roles=roles,
            id=id,
            member_key=member_key,
            preferred_member_key=preferred_member_key,
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
        '''Generates CDKTF code for importing a GoogleCloudIdentityGroupMembership resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCloudIdentityGroupMembership to import.
        :param import_from_id: The id of the existing GoogleCloudIdentityGroupMembership that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCloudIdentityGroupMembership to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dcee6a002811e6ed5d63164e63ee1a123b6ed6ed6577a4a4da717751c796da6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMemberKey")
    def put_member_key(
        self,
        *,
        id: builtins.str,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The ID of the entity. For Google-managed entities, the id must be the email address of an existing group or user. For external-identity-mapped entities, the id must be a string conforming to the Identity Source's requirements. Must be unique within a namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#id GoogleCloudIdentityGroupMembership#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param namespace: The namespace in which the entity exists. If not specified, the EntityKey represents a Google-managed entity such as a Google user or a Google Group. If specified, the EntityKey represents an external-identity-mapped group. The namespace must correspond to an identity source created in Admin Console and must be in the form of 'identitysources/{identity_source_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#namespace GoogleCloudIdentityGroupMembership#namespace}
        '''
        value = GoogleCloudIdentityGroupMembershipMemberKey(id=id, namespace=namespace)

        return typing.cast(None, jsii.invoke(self, "putMemberKey", [value]))

    @jsii.member(jsii_name="putPreferredMemberKey")
    def put_preferred_member_key(
        self,
        *,
        id: builtins.str,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The ID of the entity. For Google-managed entities, the id must be the email address of an existing group or user. For external-identity-mapped entities, the id must be a string conforming to the Identity Source's requirements. Must be unique within a namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#id GoogleCloudIdentityGroupMembership#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param namespace: The namespace in which the entity exists. If not specified, the EntityKey represents a Google-managed entity such as a Google user or a Google Group. If specified, the EntityKey represents an external-identity-mapped group. The namespace must correspond to an identity source created in Admin Console and must be in the form of 'identitysources/{identity_source_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#namespace GoogleCloudIdentityGroupMembership#namespace}
        '''
        value = GoogleCloudIdentityGroupMembershipPreferredMemberKey(
            id=id, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putPreferredMemberKey", [value]))

    @jsii.member(jsii_name="putRoles")
    def put_roles(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudIdentityGroupMembershipRoles", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422bd34812e2ae9114c132b4076f0f4232e27b1c5da3bb1b611dfe97ddba4494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRoles", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#create GoogleCloudIdentityGroupMembership#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#delete GoogleCloudIdentityGroupMembership#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#update GoogleCloudIdentityGroupMembership#update}.
        '''
        value = GoogleCloudIdentityGroupMembershipTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMemberKey")
    def reset_member_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberKey", []))

    @jsii.member(jsii_name="resetPreferredMemberKey")
    def reset_preferred_member_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredMemberKey", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="memberKey")
    def member_key(
        self,
    ) -> "GoogleCloudIdentityGroupMembershipMemberKeyOutputReference":
        return typing.cast("GoogleCloudIdentityGroupMembershipMemberKeyOutputReference", jsii.get(self, "memberKey"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="preferredMemberKey")
    def preferred_member_key(
        self,
    ) -> "GoogleCloudIdentityGroupMembershipPreferredMemberKeyOutputReference":
        return typing.cast("GoogleCloudIdentityGroupMembershipPreferredMemberKeyOutputReference", jsii.get(self, "preferredMemberKey"))

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> "GoogleCloudIdentityGroupMembershipRolesList":
        return typing.cast("GoogleCloudIdentityGroupMembershipRolesList", jsii.get(self, "roles"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleCloudIdentityGroupMembershipTimeoutsOutputReference":
        return typing.cast("GoogleCloudIdentityGroupMembershipTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

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
    @jsii.member(jsii_name="memberKeyInput")
    def member_key_input(
        self,
    ) -> typing.Optional["GoogleCloudIdentityGroupMembershipMemberKey"]:
        return typing.cast(typing.Optional["GoogleCloudIdentityGroupMembershipMemberKey"], jsii.get(self, "memberKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredMemberKeyInput")
    def preferred_member_key_input(
        self,
    ) -> typing.Optional["GoogleCloudIdentityGroupMembershipPreferredMemberKey"]:
        return typing.cast(typing.Optional["GoogleCloudIdentityGroupMembershipPreferredMemberKey"], jsii.get(self, "preferredMemberKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudIdentityGroupMembershipRoles"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudIdentityGroupMembershipRoles"]]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudIdentityGroupMembershipTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudIdentityGroupMembershipTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0daeaecb8d389926db855f4c1ca57320efc979f9a4b086f8c5be8e8bdea1e39a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e2a327ff7078df95451d2e0614fad01297c127e21ecce2ff5814d2a36cbb51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudIdentityGroupMembership.GoogleCloudIdentityGroupMembershipConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "group": "group",
        "roles": "roles",
        "id": "id",
        "member_key": "memberKey",
        "preferred_member_key": "preferredMemberKey",
        "timeouts": "timeouts",
    },
)
class GoogleCloudIdentityGroupMembershipConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        group: builtins.str,
        roles: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudIdentityGroupMembershipRoles", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        member_key: typing.Optional[typing.Union["GoogleCloudIdentityGroupMembershipMemberKey", typing.Dict[builtins.str, typing.Any]]] = None,
        preferred_member_key: typing.Optional[typing.Union["GoogleCloudIdentityGroupMembershipPreferredMemberKey", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudIdentityGroupMembershipTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param group: The name of the Group to create this membership in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#group GoogleCloudIdentityGroupMembership#group}
        :param roles: roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#roles GoogleCloudIdentityGroupMembership#roles}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#id GoogleCloudIdentityGroupMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param member_key: member_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#member_key GoogleCloudIdentityGroupMembership#member_key}
        :param preferred_member_key: preferred_member_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#preferred_member_key GoogleCloudIdentityGroupMembership#preferred_member_key}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#timeouts GoogleCloudIdentityGroupMembership#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(member_key, dict):
            member_key = GoogleCloudIdentityGroupMembershipMemberKey(**member_key)
        if isinstance(preferred_member_key, dict):
            preferred_member_key = GoogleCloudIdentityGroupMembershipPreferredMemberKey(**preferred_member_key)
        if isinstance(timeouts, dict):
            timeouts = GoogleCloudIdentityGroupMembershipTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__877abd56b4fb1d66be14559004c9b5dad129cb31da7fc4ffe7c693b47e341257)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument member_key", value=member_key, expected_type=type_hints["member_key"])
            check_type(argname="argument preferred_member_key", value=preferred_member_key, expected_type=type_hints["preferred_member_key"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group": group,
            "roles": roles,
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
        if member_key is not None:
            self._values["member_key"] = member_key
        if preferred_member_key is not None:
            self._values["preferred_member_key"] = preferred_member_key
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
    def group(self) -> builtins.str:
        '''The name of the Group to create this membership in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#group GoogleCloudIdentityGroupMembership#group}
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def roles(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudIdentityGroupMembershipRoles"]]:
        '''roles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#roles GoogleCloudIdentityGroupMembership#roles}
        '''
        result = self._values.get("roles")
        assert result is not None, "Required property 'roles' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudIdentityGroupMembershipRoles"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#id GoogleCloudIdentityGroupMembership#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_key(
        self,
    ) -> typing.Optional["GoogleCloudIdentityGroupMembershipMemberKey"]:
        '''member_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#member_key GoogleCloudIdentityGroupMembership#member_key}
        '''
        result = self._values.get("member_key")
        return typing.cast(typing.Optional["GoogleCloudIdentityGroupMembershipMemberKey"], result)

    @builtins.property
    def preferred_member_key(
        self,
    ) -> typing.Optional["GoogleCloudIdentityGroupMembershipPreferredMemberKey"]:
        '''preferred_member_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#preferred_member_key GoogleCloudIdentityGroupMembership#preferred_member_key}
        '''
        result = self._values.get("preferred_member_key")
        return typing.cast(typing.Optional["GoogleCloudIdentityGroupMembershipPreferredMemberKey"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleCloudIdentityGroupMembershipTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#timeouts GoogleCloudIdentityGroupMembership#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCloudIdentityGroupMembershipTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudIdentityGroupMembershipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudIdentityGroupMembership.GoogleCloudIdentityGroupMembershipMemberKey",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "namespace": "namespace"},
)
class GoogleCloudIdentityGroupMembershipMemberKey:
    def __init__(
        self,
        *,
        id: builtins.str,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The ID of the entity. For Google-managed entities, the id must be the email address of an existing group or user. For external-identity-mapped entities, the id must be a string conforming to the Identity Source's requirements. Must be unique within a namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#id GoogleCloudIdentityGroupMembership#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param namespace: The namespace in which the entity exists. If not specified, the EntityKey represents a Google-managed entity such as a Google user or a Google Group. If specified, the EntityKey represents an external-identity-mapped group. The namespace must correspond to an identity source created in Admin Console and must be in the form of 'identitysources/{identity_source_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#namespace GoogleCloudIdentityGroupMembership#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e72db49c767c36c3ca65444ecc2c0f3df53d0a80921cddaedcfad22390b3a94e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def id(self) -> builtins.str:
        '''The ID of the entity.

        For Google-managed entities, the id must be the email address of an existing
        group or user.

        For external-identity-mapped entities, the id must be a string conforming
        to the Identity Source's requirements.

        Must be unique within a namespace.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#id GoogleCloudIdentityGroupMembership#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace in which the entity exists.

        If not specified, the EntityKey represents a Google-managed entity
        such as a Google user or a Google Group.

        If specified, the EntityKey represents an external-identity-mapped group.
        The namespace must correspond to an identity source created in Admin Console
        and must be in the form of 'identitysources/{identity_source_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#namespace GoogleCloudIdentityGroupMembership#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudIdentityGroupMembershipMemberKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudIdentityGroupMembershipMemberKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudIdentityGroupMembership.GoogleCloudIdentityGroupMembershipMemberKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5919f241a18dd20eca48be486193bf02ffa017c8ec1f73731c725b7648f423a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d40616a2cf8abff1c1543a98580b73decdc56ae7a80c674cd4b1b40829573f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8cb3ae2de9b531fa9a45ab122098eebf8df07d5b2468e4520a69434d0baaefc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudIdentityGroupMembershipMemberKey]:
        return typing.cast(typing.Optional[GoogleCloudIdentityGroupMembershipMemberKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudIdentityGroupMembershipMemberKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7bffaea5874fad360aff808085995fdd7d4baafdf353db15a794b045e98034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudIdentityGroupMembership.GoogleCloudIdentityGroupMembershipPreferredMemberKey",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "namespace": "namespace"},
)
class GoogleCloudIdentityGroupMembershipPreferredMemberKey:
    def __init__(
        self,
        *,
        id: builtins.str,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The ID of the entity. For Google-managed entities, the id must be the email address of an existing group or user. For external-identity-mapped entities, the id must be a string conforming to the Identity Source's requirements. Must be unique within a namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#id GoogleCloudIdentityGroupMembership#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param namespace: The namespace in which the entity exists. If not specified, the EntityKey represents a Google-managed entity such as a Google user or a Google Group. If specified, the EntityKey represents an external-identity-mapped group. The namespace must correspond to an identity source created in Admin Console and must be in the form of 'identitysources/{identity_source_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#namespace GoogleCloudIdentityGroupMembership#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ef26c36cc231d521a3f0750029db7dad83090bc58053eac9243611f58bef2c)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def id(self) -> builtins.str:
        '''The ID of the entity.

        For Google-managed entities, the id must be the email address of an existing
        group or user.

        For external-identity-mapped entities, the id must be a string conforming
        to the Identity Source's requirements.

        Must be unique within a namespace.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#id GoogleCloudIdentityGroupMembership#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace in which the entity exists.

        If not specified, the EntityKey represents a Google-managed entity
        such as a Google user or a Google Group.

        If specified, the EntityKey represents an external-identity-mapped group.
        The namespace must correspond to an identity source created in Admin Console
        and must be in the form of 'identitysources/{identity_source_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#namespace GoogleCloudIdentityGroupMembership#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudIdentityGroupMembershipPreferredMemberKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudIdentityGroupMembershipPreferredMemberKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudIdentityGroupMembership.GoogleCloudIdentityGroupMembershipPreferredMemberKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__917c2d46b1ebb0e90387b9302d9d5794be0a4983443e066c08209711ef69a5b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e6f283cfc489670949b5aa30b277c058c2c2868f6d84f976d35b015e8cf19e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1f8033b6e9590a17e6c7d36b19a3c70ff9d7243769f5a5498829a6596766f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudIdentityGroupMembershipPreferredMemberKey]:
        return typing.cast(typing.Optional[GoogleCloudIdentityGroupMembershipPreferredMemberKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudIdentityGroupMembershipPreferredMemberKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e9105300b0f12c15c278f6f051523cacdd56765f1e06af776fdffb05ce52cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudIdentityGroupMembership.GoogleCloudIdentityGroupMembershipRoles",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "expiry_detail": "expiryDetail"},
)
class GoogleCloudIdentityGroupMembershipRoles:
    def __init__(
        self,
        *,
        name: builtins.str,
        expiry_detail: typing.Optional[typing.Union["GoogleCloudIdentityGroupMembershipRolesExpiryDetail", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: The name of the MembershipRole. Must be one of OWNER, MANAGER, MEMBER. Possible values: ["OWNER", "MANAGER", "MEMBER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#name GoogleCloudIdentityGroupMembership#name}
        :param expiry_detail: expiry_detail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#expiry_detail GoogleCloudIdentityGroupMembership#expiry_detail}
        '''
        if isinstance(expiry_detail, dict):
            expiry_detail = GoogleCloudIdentityGroupMembershipRolesExpiryDetail(**expiry_detail)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0555ac15ac8247382d1126cad9b8b1e1fa92ff92fe421b1742d3781e9918928)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument expiry_detail", value=expiry_detail, expected_type=type_hints["expiry_detail"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if expiry_detail is not None:
            self._values["expiry_detail"] = expiry_detail

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the MembershipRole. Must be one of OWNER, MANAGER, MEMBER. Possible values: ["OWNER", "MANAGER", "MEMBER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#name GoogleCloudIdentityGroupMembership#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiry_detail(
        self,
    ) -> typing.Optional["GoogleCloudIdentityGroupMembershipRolesExpiryDetail"]:
        '''expiry_detail block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#expiry_detail GoogleCloudIdentityGroupMembership#expiry_detail}
        '''
        result = self._values.get("expiry_detail")
        return typing.cast(typing.Optional["GoogleCloudIdentityGroupMembershipRolesExpiryDetail"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudIdentityGroupMembershipRoles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudIdentityGroupMembership.GoogleCloudIdentityGroupMembershipRolesExpiryDetail",
    jsii_struct_bases=[],
    name_mapping={"expire_time": "expireTime"},
)
class GoogleCloudIdentityGroupMembershipRolesExpiryDetail:
    def __init__(self, *, expire_time: builtins.str) -> None:
        '''
        :param expire_time: The time at which the MembershipRole will expire. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#expire_time GoogleCloudIdentityGroupMembership#expire_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d477ea5e28f5db9d5e589bdc0ce6288be928bb994aea770588ed67276821f1e0)
            check_type(argname="argument expire_time", value=expire_time, expected_type=type_hints["expire_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expire_time": expire_time,
        }

    @builtins.property
    def expire_time(self) -> builtins.str:
        '''The time at which the MembershipRole will expire.

        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond
        resolution and up to nine fractional digits.

        Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#expire_time GoogleCloudIdentityGroupMembership#expire_time}
        '''
        result = self._values.get("expire_time")
        assert result is not None, "Required property 'expire_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudIdentityGroupMembershipRolesExpiryDetail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudIdentityGroupMembershipRolesExpiryDetailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudIdentityGroupMembership.GoogleCloudIdentityGroupMembershipRolesExpiryDetailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__986dbf73943e0c5b68d7d148ef854cad691d14404bd6c190695a387e0cd8429a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="expireTimeInput")
    def expire_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expireTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="expireTime")
    def expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireTime"))

    @expire_time.setter
    def expire_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24350d47030f3990b35f1365dd1a1c00306c2bc2fb7412551b97522632f450ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudIdentityGroupMembershipRolesExpiryDetail]:
        return typing.cast(typing.Optional[GoogleCloudIdentityGroupMembershipRolesExpiryDetail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudIdentityGroupMembershipRolesExpiryDetail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd16c967459a9dd1d9b17602b87b288f80a6b8ce16aca547b8d8d9384a21a13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudIdentityGroupMembershipRolesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudIdentityGroupMembership.GoogleCloudIdentityGroupMembershipRolesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63993193e7368e9b912978971fcd962e1cfc4fa0f38fadd023f0d23739858e2f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudIdentityGroupMembershipRolesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd83b9f7182a264cd626f2095176e9848debfb9d4e8cd98a8c355c0d1d0f9a42)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudIdentityGroupMembershipRolesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f4c53bfac9ce36a0d00b09542c3d3b97c559b42ff9565632c65812c0cde366)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58b02e056d1c849e3e86edda1abb3fef15084369d0a11460fcc3cf6b807dc426)
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
            type_hints = typing.get_type_hints(_typecheckingstub__505b2a2e7bd86df16dca8d8fc2f244c7f324315c733eba81d03e09e261ccb78e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudIdentityGroupMembershipRoles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudIdentityGroupMembershipRoles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudIdentityGroupMembershipRoles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c2778db87754898c0a84e3b8256367ec78843c5edf394ef3f92511b7c816d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudIdentityGroupMembershipRolesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudIdentityGroupMembership.GoogleCloudIdentityGroupMembershipRolesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e8c0cdab4839f4edcca1eae3c01ca154ad4aeb3ffa89cd41224635bc79e8644)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExpiryDetail")
    def put_expiry_detail(self, *, expire_time: builtins.str) -> None:
        '''
        :param expire_time: The time at which the MembershipRole will expire. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#expire_time GoogleCloudIdentityGroupMembership#expire_time}
        '''
        value = GoogleCloudIdentityGroupMembershipRolesExpiryDetail(
            expire_time=expire_time
        )

        return typing.cast(None, jsii.invoke(self, "putExpiryDetail", [value]))

    @jsii.member(jsii_name="resetExpiryDetail")
    def reset_expiry_detail(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiryDetail", []))

    @builtins.property
    @jsii.member(jsii_name="expiryDetail")
    def expiry_detail(
        self,
    ) -> GoogleCloudIdentityGroupMembershipRolesExpiryDetailOutputReference:
        return typing.cast(GoogleCloudIdentityGroupMembershipRolesExpiryDetailOutputReference, jsii.get(self, "expiryDetail"))

    @builtins.property
    @jsii.member(jsii_name="expiryDetailInput")
    def expiry_detail_input(
        self,
    ) -> typing.Optional[GoogleCloudIdentityGroupMembershipRolesExpiryDetail]:
        return typing.cast(typing.Optional[GoogleCloudIdentityGroupMembershipRolesExpiryDetail], jsii.get(self, "expiryDetailInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f8e9388b36b03640fa492e5b5da101d9a8ea353cd96b87a02a23606e760d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudIdentityGroupMembershipRoles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudIdentityGroupMembershipRoles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudIdentityGroupMembershipRoles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f36abe2e1444a45c4fae883129ce3f72d0049d34a4e082047c016d1d32eecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudIdentityGroupMembership.GoogleCloudIdentityGroupMembershipTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCloudIdentityGroupMembershipTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#create GoogleCloudIdentityGroupMembership#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#delete GoogleCloudIdentityGroupMembership#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#update GoogleCloudIdentityGroupMembership#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2051c13777c95424a4117323e96625d62cd40e6aa9c37ce9e78e93b78902a16)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#create GoogleCloudIdentityGroupMembership#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#delete GoogleCloudIdentityGroupMembership#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_identity_group_membership#update GoogleCloudIdentityGroupMembership#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudIdentityGroupMembershipTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudIdentityGroupMembershipTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudIdentityGroupMembership.GoogleCloudIdentityGroupMembershipTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b21d391cc4265e0f3ed62beff9814da1bc2f1f8df13d0737a3a3633de0b55581)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7043e8da72e18a3e60212b0b2fb3719348d8443807d7ba18394290fa730520d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15069d920924decdca5700eff252f0876ee8f9654729e51b31ae724ba25741bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93776c66775f2a223241f7c94dc9babe519621d73b87b27049b8919cbe101056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudIdentityGroupMembershipTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudIdentityGroupMembershipTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudIdentityGroupMembershipTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f92a3c9b3b13410ed8096d112e384b4eb0d824f12b684e44e8e3d64e759eb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCloudIdentityGroupMembership",
    "GoogleCloudIdentityGroupMembershipConfig",
    "GoogleCloudIdentityGroupMembershipMemberKey",
    "GoogleCloudIdentityGroupMembershipMemberKeyOutputReference",
    "GoogleCloudIdentityGroupMembershipPreferredMemberKey",
    "GoogleCloudIdentityGroupMembershipPreferredMemberKeyOutputReference",
    "GoogleCloudIdentityGroupMembershipRoles",
    "GoogleCloudIdentityGroupMembershipRolesExpiryDetail",
    "GoogleCloudIdentityGroupMembershipRolesExpiryDetailOutputReference",
    "GoogleCloudIdentityGroupMembershipRolesList",
    "GoogleCloudIdentityGroupMembershipRolesOutputReference",
    "GoogleCloudIdentityGroupMembershipTimeouts",
    "GoogleCloudIdentityGroupMembershipTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__8940681f98a3eeb6dc87a4554a6a09babf451bb3d3b2fb2879ed621d79ac2d8a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    group: builtins.str,
    roles: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudIdentityGroupMembershipRoles, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    member_key: typing.Optional[typing.Union[GoogleCloudIdentityGroupMembershipMemberKey, typing.Dict[builtins.str, typing.Any]]] = None,
    preferred_member_key: typing.Optional[typing.Union[GoogleCloudIdentityGroupMembershipPreferredMemberKey, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudIdentityGroupMembershipTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3dcee6a002811e6ed5d63164e63ee1a123b6ed6ed6577a4a4da717751c796da6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422bd34812e2ae9114c132b4076f0f4232e27b1c5da3bb1b611dfe97ddba4494(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudIdentityGroupMembershipRoles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0daeaecb8d389926db855f4c1ca57320efc979f9a4b086f8c5be8e8bdea1e39a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e2a327ff7078df95451d2e0614fad01297c127e21ecce2ff5814d2a36cbb51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877abd56b4fb1d66be14559004c9b5dad129cb31da7fc4ffe7c693b47e341257(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    group: builtins.str,
    roles: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudIdentityGroupMembershipRoles, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    member_key: typing.Optional[typing.Union[GoogleCloudIdentityGroupMembershipMemberKey, typing.Dict[builtins.str, typing.Any]]] = None,
    preferred_member_key: typing.Optional[typing.Union[GoogleCloudIdentityGroupMembershipPreferredMemberKey, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudIdentityGroupMembershipTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e72db49c767c36c3ca65444ecc2c0f3df53d0a80921cddaedcfad22390b3a94e(
    *,
    id: builtins.str,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5919f241a18dd20eca48be486193bf02ffa017c8ec1f73731c725b7648f423a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d40616a2cf8abff1c1543a98580b73decdc56ae7a80c674cd4b1b40829573f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8cb3ae2de9b531fa9a45ab122098eebf8df07d5b2468e4520a69434d0baaefc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7bffaea5874fad360aff808085995fdd7d4baafdf353db15a794b045e98034(
    value: typing.Optional[GoogleCloudIdentityGroupMembershipMemberKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ef26c36cc231d521a3f0750029db7dad83090bc58053eac9243611f58bef2c(
    *,
    id: builtins.str,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917c2d46b1ebb0e90387b9302d9d5794be0a4983443e066c08209711ef69a5b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e6f283cfc489670949b5aa30b277c058c2c2868f6d84f976d35b015e8cf19e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1f8033b6e9590a17e6c7d36b19a3c70ff9d7243769f5a5498829a6596766f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e9105300b0f12c15c278f6f051523cacdd56765f1e06af776fdffb05ce52cf(
    value: typing.Optional[GoogleCloudIdentityGroupMembershipPreferredMemberKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0555ac15ac8247382d1126cad9b8b1e1fa92ff92fe421b1742d3781e9918928(
    *,
    name: builtins.str,
    expiry_detail: typing.Optional[typing.Union[GoogleCloudIdentityGroupMembershipRolesExpiryDetail, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d477ea5e28f5db9d5e589bdc0ce6288be928bb994aea770588ed67276821f1e0(
    *,
    expire_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986dbf73943e0c5b68d7d148ef854cad691d14404bd6c190695a387e0cd8429a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24350d47030f3990b35f1365dd1a1c00306c2bc2fb7412551b97522632f450ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd16c967459a9dd1d9b17602b87b288f80a6b8ce16aca547b8d8d9384a21a13(
    value: typing.Optional[GoogleCloudIdentityGroupMembershipRolesExpiryDetail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63993193e7368e9b912978971fcd962e1cfc4fa0f38fadd023f0d23739858e2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd83b9f7182a264cd626f2095176e9848debfb9d4e8cd98a8c355c0d1d0f9a42(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f4c53bfac9ce36a0d00b09542c3d3b97c559b42ff9565632c65812c0cde366(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b02e056d1c849e3e86edda1abb3fef15084369d0a11460fcc3cf6b807dc426(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505b2a2e7bd86df16dca8d8fc2f244c7f324315c733eba81d03e09e261ccb78e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c2778db87754898c0a84e3b8256367ec78843c5edf394ef3f92511b7c816d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudIdentityGroupMembershipRoles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8c0cdab4839f4edcca1eae3c01ca154ad4aeb3ffa89cd41224635bc79e8644(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f8e9388b36b03640fa492e5b5da101d9a8ea353cd96b87a02a23606e760d20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f36abe2e1444a45c4fae883129ce3f72d0049d34a4e082047c016d1d32eecb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudIdentityGroupMembershipRoles]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2051c13777c95424a4117323e96625d62cd40e6aa9c37ce9e78e93b78902a16(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21d391cc4265e0f3ed62beff9814da1bc2f1f8df13d0737a3a3633de0b55581(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7043e8da72e18a3e60212b0b2fb3719348d8443807d7ba18394290fa730520d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15069d920924decdca5700eff252f0876ee8f9654729e51b31ae724ba25741bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93776c66775f2a223241f7c94dc9babe519621d73b87b27049b8919cbe101056(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f92a3c9b3b13410ed8096d112e384b4eb0d824f12b684e44e8e3d64e759eb7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudIdentityGroupMembershipTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
