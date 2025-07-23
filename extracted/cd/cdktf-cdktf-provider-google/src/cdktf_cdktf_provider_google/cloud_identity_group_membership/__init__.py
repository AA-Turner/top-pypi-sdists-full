r'''
# `google_cloud_identity_group_membership`

Refer to the Terraform Registry for docs: [`google_cloud_identity_group_membership`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership).
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


class CloudIdentityGroupMembership(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudIdentityGroupMembership.CloudIdentityGroupMembership",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership google_cloud_identity_group_membership}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        group: builtins.str,
        roles: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudIdentityGroupMembershipRoles", typing.Dict[builtins.str, typing.Any]]]],
        create_ignore_already_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        preferred_member_key: typing.Optional[typing.Union["CloudIdentityGroupMembershipPreferredMemberKey", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CloudIdentityGroupMembershipTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership google_cloud_identity_group_membership} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param group: The name of the Group to create this membership in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#group CloudIdentityGroupMembership#group}
        :param roles: roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#roles CloudIdentityGroupMembership#roles}
        :param create_ignore_already_exists: If set to true, skip group member creation if a membership with the same name already exists. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#create_ignore_already_exists CloudIdentityGroupMembership#create_ignore_already_exists}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#id CloudIdentityGroupMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param preferred_member_key: preferred_member_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#preferred_member_key CloudIdentityGroupMembership#preferred_member_key}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#timeouts CloudIdentityGroupMembership#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829b5a8f2cb1d7a042c1ab09abc15b5d6027219a5557d7ed5984c8562c41a8be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudIdentityGroupMembershipConfig(
            group=group,
            roles=roles,
            create_ignore_already_exists=create_ignore_already_exists,
            id=id,
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
        '''Generates CDKTF code for importing a CloudIdentityGroupMembership resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudIdentityGroupMembership to import.
        :param import_from_id: The id of the existing CloudIdentityGroupMembership that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudIdentityGroupMembership to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c86e4abb41ac9708c7ced3e8cd9f6f4a82707e2cfa412d912dac2faa002950b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPreferredMemberKey")
    def put_preferred_member_key(
        self,
        *,
        id: builtins.str,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The ID of the entity. For Google-managed entities, the id must be the email address of an existing group or user. For external-identity-mapped entities, the id must be a string conforming to the Identity Source's requirements. Must be unique within a namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#id CloudIdentityGroupMembership#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param namespace: The namespace in which the entity exists. If not specified, the EntityKey represents a Google-managed entity such as a Google user or a Google Group. If specified, the EntityKey represents an external-identity-mapped group. The namespace must correspond to an identity source created in Admin Console and must be in the form of 'identitysources/{identity_source_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#namespace CloudIdentityGroupMembership#namespace}
        '''
        value = CloudIdentityGroupMembershipPreferredMemberKey(
            id=id, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putPreferredMemberKey", [value]))

    @jsii.member(jsii_name="putRoles")
    def put_roles(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudIdentityGroupMembershipRoles", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a746a739fd1254b2a0347070cca5c3d5377acc1942a97cc8682123a01373e14e)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#create CloudIdentityGroupMembership#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#delete CloudIdentityGroupMembership#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#update CloudIdentityGroupMembership#update}.
        '''
        value = CloudIdentityGroupMembershipTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCreateIgnoreAlreadyExists")
    def reset_create_ignore_already_exists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateIgnoreAlreadyExists", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="preferredMemberKey")
    def preferred_member_key(
        self,
    ) -> "CloudIdentityGroupMembershipPreferredMemberKeyOutputReference":
        return typing.cast("CloudIdentityGroupMembershipPreferredMemberKeyOutputReference", jsii.get(self, "preferredMemberKey"))

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> "CloudIdentityGroupMembershipRolesList":
        return typing.cast("CloudIdentityGroupMembershipRolesList", jsii.get(self, "roles"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudIdentityGroupMembershipTimeoutsOutputReference":
        return typing.cast("CloudIdentityGroupMembershipTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="createIgnoreAlreadyExistsInput")
    def create_ignore_already_exists_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createIgnoreAlreadyExistsInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredMemberKeyInput")
    def preferred_member_key_input(
        self,
    ) -> typing.Optional["CloudIdentityGroupMembershipPreferredMemberKey"]:
        return typing.cast(typing.Optional["CloudIdentityGroupMembershipPreferredMemberKey"], jsii.get(self, "preferredMemberKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudIdentityGroupMembershipRoles"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudIdentityGroupMembershipRoles"]]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudIdentityGroupMembershipTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudIdentityGroupMembershipTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="createIgnoreAlreadyExists")
    def create_ignore_already_exists(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createIgnoreAlreadyExists"))

    @create_ignore_already_exists.setter
    def create_ignore_already_exists(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b5f6db9aaa18eb1c956214f1e8577785896473b9a7eef456177cb18c33ecdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createIgnoreAlreadyExists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__384233c53813aac26583d841a2ad5ea8a34ba1461230b95ce17b39c7d3d7b5b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c5d574ead0d4d1b664e54080605d56fc5bd5df5c791477efdf03e7e824d1856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudIdentityGroupMembership.CloudIdentityGroupMembershipConfig",
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
        "create_ignore_already_exists": "createIgnoreAlreadyExists",
        "id": "id",
        "preferred_member_key": "preferredMemberKey",
        "timeouts": "timeouts",
    },
)
class CloudIdentityGroupMembershipConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        roles: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudIdentityGroupMembershipRoles", typing.Dict[builtins.str, typing.Any]]]],
        create_ignore_already_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        preferred_member_key: typing.Optional[typing.Union["CloudIdentityGroupMembershipPreferredMemberKey", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CloudIdentityGroupMembershipTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param group: The name of the Group to create this membership in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#group CloudIdentityGroupMembership#group}
        :param roles: roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#roles CloudIdentityGroupMembership#roles}
        :param create_ignore_already_exists: If set to true, skip group member creation if a membership with the same name already exists. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#create_ignore_already_exists CloudIdentityGroupMembership#create_ignore_already_exists}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#id CloudIdentityGroupMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param preferred_member_key: preferred_member_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#preferred_member_key CloudIdentityGroupMembership#preferred_member_key}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#timeouts CloudIdentityGroupMembership#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(preferred_member_key, dict):
            preferred_member_key = CloudIdentityGroupMembershipPreferredMemberKey(**preferred_member_key)
        if isinstance(timeouts, dict):
            timeouts = CloudIdentityGroupMembershipTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__979afb079c3c1bdb50e4181e2c8e136f18129a9fb113f5cf70304390beec9aed)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument create_ignore_already_exists", value=create_ignore_already_exists, expected_type=type_hints["create_ignore_already_exists"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
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
        if create_ignore_already_exists is not None:
            self._values["create_ignore_already_exists"] = create_ignore_already_exists
        if id is not None:
            self._values["id"] = id
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#group CloudIdentityGroupMembership#group}
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def roles(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudIdentityGroupMembershipRoles"]]:
        '''roles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#roles CloudIdentityGroupMembership#roles}
        '''
        result = self._values.get("roles")
        assert result is not None, "Required property 'roles' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudIdentityGroupMembershipRoles"]], result)

    @builtins.property
    def create_ignore_already_exists(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, skip group member creation if a membership with the same name already exists.

        Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#create_ignore_already_exists CloudIdentityGroupMembership#create_ignore_already_exists}
        '''
        result = self._values.get("create_ignore_already_exists")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#id CloudIdentityGroupMembership#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_member_key(
        self,
    ) -> typing.Optional["CloudIdentityGroupMembershipPreferredMemberKey"]:
        '''preferred_member_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#preferred_member_key CloudIdentityGroupMembership#preferred_member_key}
        '''
        result = self._values.get("preferred_member_key")
        return typing.cast(typing.Optional["CloudIdentityGroupMembershipPreferredMemberKey"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudIdentityGroupMembershipTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#timeouts CloudIdentityGroupMembership#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudIdentityGroupMembershipTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudIdentityGroupMembershipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudIdentityGroupMembership.CloudIdentityGroupMembershipPreferredMemberKey",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "namespace": "namespace"},
)
class CloudIdentityGroupMembershipPreferredMemberKey:
    def __init__(
        self,
        *,
        id: builtins.str,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The ID of the entity. For Google-managed entities, the id must be the email address of an existing group or user. For external-identity-mapped entities, the id must be a string conforming to the Identity Source's requirements. Must be unique within a namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#id CloudIdentityGroupMembership#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param namespace: The namespace in which the entity exists. If not specified, the EntityKey represents a Google-managed entity such as a Google user or a Google Group. If specified, the EntityKey represents an external-identity-mapped group. The namespace must correspond to an identity source created in Admin Console and must be in the form of 'identitysources/{identity_source_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#namespace CloudIdentityGroupMembership#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c1cb6a8db1e2500583cd40695ae54c27dd0d518aa91d1d67b4c86dbcb8e39e1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#id CloudIdentityGroupMembership#id}

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#namespace CloudIdentityGroupMembership#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudIdentityGroupMembershipPreferredMemberKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudIdentityGroupMembershipPreferredMemberKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudIdentityGroupMembership.CloudIdentityGroupMembershipPreferredMemberKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bc80677deb79ab559a2f7f0b409fe97f6c3427fc390dd85d19ab24d75fda7ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccd2830ecc2b28d82d57dd3999baa392d577e1ed9a991a27bf3be15f69111d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48abe2dd8d92dcadc0e6fc13aaaa0f4cd1d4439630d613c0f8f9a9d4b12619d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudIdentityGroupMembershipPreferredMemberKey]:
        return typing.cast(typing.Optional[CloudIdentityGroupMembershipPreferredMemberKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudIdentityGroupMembershipPreferredMemberKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a911cf428031bccdba14a38d37a4ef37b78f28288eb358f0cd17222a9ea33455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudIdentityGroupMembership.CloudIdentityGroupMembershipRoles",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "expiry_detail": "expiryDetail"},
)
class CloudIdentityGroupMembershipRoles:
    def __init__(
        self,
        *,
        name: builtins.str,
        expiry_detail: typing.Optional[typing.Union["CloudIdentityGroupMembershipRolesExpiryDetail", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: The name of the MembershipRole. Must be one of OWNER, MANAGER, MEMBER. Possible values: ["OWNER", "MANAGER", "MEMBER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#name CloudIdentityGroupMembership#name}
        :param expiry_detail: expiry_detail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#expiry_detail CloudIdentityGroupMembership#expiry_detail}
        '''
        if isinstance(expiry_detail, dict):
            expiry_detail = CloudIdentityGroupMembershipRolesExpiryDetail(**expiry_detail)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f982bec5e34422be937e2d50145809b99c518ac8679fdd3afab84deb3b924a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#name CloudIdentityGroupMembership#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiry_detail(
        self,
    ) -> typing.Optional["CloudIdentityGroupMembershipRolesExpiryDetail"]:
        '''expiry_detail block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#expiry_detail CloudIdentityGroupMembership#expiry_detail}
        '''
        result = self._values.get("expiry_detail")
        return typing.cast(typing.Optional["CloudIdentityGroupMembershipRolesExpiryDetail"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudIdentityGroupMembershipRoles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudIdentityGroupMembership.CloudIdentityGroupMembershipRolesExpiryDetail",
    jsii_struct_bases=[],
    name_mapping={"expire_time": "expireTime"},
)
class CloudIdentityGroupMembershipRolesExpiryDetail:
    def __init__(self, *, expire_time: builtins.str) -> None:
        '''
        :param expire_time: The time at which the MembershipRole will expire. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#expire_time CloudIdentityGroupMembership#expire_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9b218ba8da4eb1a96037596b5f55a3dc0c4f3a1ce77d1d8f4eca366c283730)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#expire_time CloudIdentityGroupMembership#expire_time}
        '''
        result = self._values.get("expire_time")
        assert result is not None, "Required property 'expire_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudIdentityGroupMembershipRolesExpiryDetail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudIdentityGroupMembershipRolesExpiryDetailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudIdentityGroupMembership.CloudIdentityGroupMembershipRolesExpiryDetailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9558d942b430d6952ff2d2c29fa0dee6afc9f79d466899eb00b34595f8f3e0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0110613a98c74ca2df05410e00d5ff463f4d9d910502e56ab2e7be85725dc78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudIdentityGroupMembershipRolesExpiryDetail]:
        return typing.cast(typing.Optional[CloudIdentityGroupMembershipRolesExpiryDetail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudIdentityGroupMembershipRolesExpiryDetail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8dd074f6c5ad6c224e3d175460652c74f52a085a224a42b964c987e4ced9129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudIdentityGroupMembershipRolesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudIdentityGroupMembership.CloudIdentityGroupMembershipRolesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a12d40172d423e87366cccb41ea8385ac710968f6f4d87a8b9195a338f55b965)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudIdentityGroupMembershipRolesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8726d34bf0b602ed6e88f4c3ec7acc6837ffbca14f2363d73d0746b3eab9b98)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudIdentityGroupMembershipRolesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__074b719943b0426032bde65b8d47856b4d89f248d00cf80c6c15e152d6c37c88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28e13f35034e404f4a2a5f72b2f739935b5f012b408a3dad06226ea352e26ac5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65489afe250577a149c1f9ad9c4f4dfbee3d4c871bd973c0c405c36bf47b1055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudIdentityGroupMembershipRoles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudIdentityGroupMembershipRoles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudIdentityGroupMembershipRoles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47b5247dcb34ebb9c91a29e0e3cca3a57f99f033d7d67af1c3427a4bfb63a4cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudIdentityGroupMembershipRolesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudIdentityGroupMembership.CloudIdentityGroupMembershipRolesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b962b4b30e6d272461038a062e0100cbf67b93ddb975d186afd00537f8227df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExpiryDetail")
    def put_expiry_detail(self, *, expire_time: builtins.str) -> None:
        '''
        :param expire_time: The time at which the MembershipRole will expire. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#expire_time CloudIdentityGroupMembership#expire_time}
        '''
        value = CloudIdentityGroupMembershipRolesExpiryDetail(expire_time=expire_time)

        return typing.cast(None, jsii.invoke(self, "putExpiryDetail", [value]))

    @jsii.member(jsii_name="resetExpiryDetail")
    def reset_expiry_detail(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiryDetail", []))

    @builtins.property
    @jsii.member(jsii_name="expiryDetail")
    def expiry_detail(
        self,
    ) -> CloudIdentityGroupMembershipRolesExpiryDetailOutputReference:
        return typing.cast(CloudIdentityGroupMembershipRolesExpiryDetailOutputReference, jsii.get(self, "expiryDetail"))

    @builtins.property
    @jsii.member(jsii_name="expiryDetailInput")
    def expiry_detail_input(
        self,
    ) -> typing.Optional[CloudIdentityGroupMembershipRolesExpiryDetail]:
        return typing.cast(typing.Optional[CloudIdentityGroupMembershipRolesExpiryDetail], jsii.get(self, "expiryDetailInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ac5fcf6b017431052f650706eded92114299198c277e933716cf5afbda964cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudIdentityGroupMembershipRoles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudIdentityGroupMembershipRoles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudIdentityGroupMembershipRoles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742035f07c98cd203e8c2811fd34986ddf514ef23571bf211dee938bc869b7fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudIdentityGroupMembership.CloudIdentityGroupMembershipTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudIdentityGroupMembershipTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#create CloudIdentityGroupMembership#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#delete CloudIdentityGroupMembership#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#update CloudIdentityGroupMembership#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59150ceda146ff2f53c1e4ea4ed4975a0d898dd5471157ebf7c29aa52f921ffb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#create CloudIdentityGroupMembership#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#delete CloudIdentityGroupMembership#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_identity_group_membership#update CloudIdentityGroupMembership#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudIdentityGroupMembershipTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudIdentityGroupMembershipTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudIdentityGroupMembership.CloudIdentityGroupMembershipTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48c186e900bac7cff4f34d1da184965dd975b8beb05dc92073c62954eef99f54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c069487b7071681d5269a1b39333ac06516006259699d7df81fc499403edf78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08bca9ba07ea35f7b83a9d2e7570097353c6427bd0df59c617a6f0faaa0464c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a851a13342d46083c35c6ede2025ea10f25d41cb035e448b557e6144c309478c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudIdentityGroupMembershipTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudIdentityGroupMembershipTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudIdentityGroupMembershipTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963e534d0d1079561881ecb04bbf83b0c5739ac793f0b03973398930fea30304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudIdentityGroupMembership",
    "CloudIdentityGroupMembershipConfig",
    "CloudIdentityGroupMembershipPreferredMemberKey",
    "CloudIdentityGroupMembershipPreferredMemberKeyOutputReference",
    "CloudIdentityGroupMembershipRoles",
    "CloudIdentityGroupMembershipRolesExpiryDetail",
    "CloudIdentityGroupMembershipRolesExpiryDetailOutputReference",
    "CloudIdentityGroupMembershipRolesList",
    "CloudIdentityGroupMembershipRolesOutputReference",
    "CloudIdentityGroupMembershipTimeouts",
    "CloudIdentityGroupMembershipTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__829b5a8f2cb1d7a042c1ab09abc15b5d6027219a5557d7ed5984c8562c41a8be(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    group: builtins.str,
    roles: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudIdentityGroupMembershipRoles, typing.Dict[builtins.str, typing.Any]]]],
    create_ignore_already_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    preferred_member_key: typing.Optional[typing.Union[CloudIdentityGroupMembershipPreferredMemberKey, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CloudIdentityGroupMembershipTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6c86e4abb41ac9708c7ced3e8cd9f6f4a82707e2cfa412d912dac2faa002950b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a746a739fd1254b2a0347070cca5c3d5377acc1942a97cc8682123a01373e14e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudIdentityGroupMembershipRoles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b5f6db9aaa18eb1c956214f1e8577785896473b9a7eef456177cb18c33ecdf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__384233c53813aac26583d841a2ad5ea8a34ba1461230b95ce17b39c7d3d7b5b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5d574ead0d4d1b664e54080605d56fc5bd5df5c791477efdf03e7e824d1856(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979afb079c3c1bdb50e4181e2c8e136f18129a9fb113f5cf70304390beec9aed(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    group: builtins.str,
    roles: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudIdentityGroupMembershipRoles, typing.Dict[builtins.str, typing.Any]]]],
    create_ignore_already_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    preferred_member_key: typing.Optional[typing.Union[CloudIdentityGroupMembershipPreferredMemberKey, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CloudIdentityGroupMembershipTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1cb6a8db1e2500583cd40695ae54c27dd0d518aa91d1d67b4c86dbcb8e39e1(
    *,
    id: builtins.str,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc80677deb79ab559a2f7f0b409fe97f6c3427fc390dd85d19ab24d75fda7ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd2830ecc2b28d82d57dd3999baa392d577e1ed9a991a27bf3be15f69111d0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48abe2dd8d92dcadc0e6fc13aaaa0f4cd1d4439630d613c0f8f9a9d4b12619d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a911cf428031bccdba14a38d37a4ef37b78f28288eb358f0cd17222a9ea33455(
    value: typing.Optional[CloudIdentityGroupMembershipPreferredMemberKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f982bec5e34422be937e2d50145809b99c518ac8679fdd3afab84deb3b924a(
    *,
    name: builtins.str,
    expiry_detail: typing.Optional[typing.Union[CloudIdentityGroupMembershipRolesExpiryDetail, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9b218ba8da4eb1a96037596b5f55a3dc0c4f3a1ce77d1d8f4eca366c283730(
    *,
    expire_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9558d942b430d6952ff2d2c29fa0dee6afc9f79d466899eb00b34595f8f3e0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0110613a98c74ca2df05410e00d5ff463f4d9d910502e56ab2e7be85725dc78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8dd074f6c5ad6c224e3d175460652c74f52a085a224a42b964c987e4ced9129(
    value: typing.Optional[CloudIdentityGroupMembershipRolesExpiryDetail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12d40172d423e87366cccb41ea8385ac710968f6f4d87a8b9195a338f55b965(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8726d34bf0b602ed6e88f4c3ec7acc6837ffbca14f2363d73d0746b3eab9b98(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074b719943b0426032bde65b8d47856b4d89f248d00cf80c6c15e152d6c37c88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e13f35034e404f4a2a5f72b2f739935b5f012b408a3dad06226ea352e26ac5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65489afe250577a149c1f9ad9c4f4dfbee3d4c871bd973c0c405c36bf47b1055(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47b5247dcb34ebb9c91a29e0e3cca3a57f99f033d7d67af1c3427a4bfb63a4cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudIdentityGroupMembershipRoles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b962b4b30e6d272461038a062e0100cbf67b93ddb975d186afd00537f8227df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5fcf6b017431052f650706eded92114299198c277e933716cf5afbda964cfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742035f07c98cd203e8c2811fd34986ddf514ef23571bf211dee938bc869b7fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudIdentityGroupMembershipRoles]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59150ceda146ff2f53c1e4ea4ed4975a0d898dd5471157ebf7c29aa52f921ffb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c186e900bac7cff4f34d1da184965dd975b8beb05dc92073c62954eef99f54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c069487b7071681d5269a1b39333ac06516006259699d7df81fc499403edf78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08bca9ba07ea35f7b83a9d2e7570097353c6427bd0df59c617a6f0faaa0464c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a851a13342d46083c35c6ede2025ea10f25d41cb035e448b557e6144c309478c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963e534d0d1079561881ecb04bbf83b0c5739ac793f0b03973398930fea30304(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudIdentityGroupMembershipTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
