r'''
# `github_team`

Refer to the Terraform Registry for docs: [`github_team`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team).
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


class Team(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.team.Team",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team github_team}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        create_default_maintainer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ldap_dn: typing.Optional[builtins.str] = None,
        parent_team_id: typing.Optional[builtins.str] = None,
        parent_team_read_id: typing.Optional[builtins.str] = None,
        parent_team_read_slug: typing.Optional[builtins.str] = None,
        privacy: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team github_team} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the team. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#name Team#name}
        :param create_default_maintainer: Adds a default maintainer to the team. Adds the creating user to the team when 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#create_default_maintainer Team#create_default_maintainer}
        :param description: A description of the team. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#description Team#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#id Team#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ldap_dn: The LDAP Distinguished Name of the group where membership will be synchronized. Only available in GitHub Enterprise Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#ldap_dn Team#ldap_dn}
        :param parent_team_id: The ID or slug of the parent team, if this is a nested team. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#parent_team_id Team#parent_team_id}
        :param parent_team_read_id: The id of the parent team read in Github. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#parent_team_read_id Team#parent_team_read_id}
        :param parent_team_read_slug: The id of the parent team read in Github. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#parent_team_read_slug Team#parent_team_read_slug}
        :param privacy: The level of privacy for the team. Must be one of 'secret' or 'closed'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#privacy Team#privacy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca448c41b9f6dc955ef80a805cab1cb3ed4f5b0c5c4db093e32387f385ff10b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = TeamConfig(
            name=name,
            create_default_maintainer=create_default_maintainer,
            description=description,
            id=id,
            ldap_dn=ldap_dn,
            parent_team_id=parent_team_id,
            parent_team_read_id=parent_team_read_id,
            parent_team_read_slug=parent_team_read_slug,
            privacy=privacy,
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
        '''Generates CDKTF code for importing a Team resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Team to import.
        :param import_from_id: The id of the existing Team that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Team to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e6458102f84c8ac1b2ded755f46a8cd3a0abfa324384cd105ec6532b6621563)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetCreateDefaultMaintainer")
    def reset_create_default_maintainer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateDefaultMaintainer", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLdapDn")
    def reset_ldap_dn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLdapDn", []))

    @jsii.member(jsii_name="resetParentTeamId")
    def reset_parent_team_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParentTeamId", []))

    @jsii.member(jsii_name="resetParentTeamReadId")
    def reset_parent_team_read_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParentTeamReadId", []))

    @jsii.member(jsii_name="resetParentTeamReadSlug")
    def reset_parent_team_read_slug(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParentTeamReadSlug", []))

    @jsii.member(jsii_name="resetPrivacy")
    def reset_privacy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivacy", []))

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
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="membersCount")
    def members_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "membersCount"))

    @builtins.property
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeId"))

    @builtins.property
    @jsii.member(jsii_name="slug")
    def slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slug"))

    @builtins.property
    @jsii.member(jsii_name="createDefaultMaintainerInput")
    def create_default_maintainer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createDefaultMaintainerInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ldapDnInput")
    def ldap_dn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ldapDnInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parentTeamIdInput")
    def parent_team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentTeamIdInput"))

    @builtins.property
    @jsii.member(jsii_name="parentTeamReadIdInput")
    def parent_team_read_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentTeamReadIdInput"))

    @builtins.property
    @jsii.member(jsii_name="parentTeamReadSlugInput")
    def parent_team_read_slug_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentTeamReadSlugInput"))

    @builtins.property
    @jsii.member(jsii_name="privacyInput")
    def privacy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privacyInput"))

    @builtins.property
    @jsii.member(jsii_name="createDefaultMaintainer")
    def create_default_maintainer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createDefaultMaintainer"))

    @create_default_maintainer.setter
    def create_default_maintainer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862ef8eb06d2c76c2ba5433f21ff71e9f8dd1585051cbb18367b5b4b8af0f0c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createDefaultMaintainer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b976fe33bc6083fb7b0ca946b844bc4e20b4b8e8736cd4cd51c997084002a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc18b193d1fa5a2c5c81f741b77037276ae0bee5016c349469aefc36d34e85d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ldapDn")
    def ldap_dn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ldapDn"))

    @ldap_dn.setter
    def ldap_dn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab7e4949bd85d85e39b252323c6e82b63336a6e4046b9c7bae800dc683ce84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ldapDn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3a056c0ad8a48baffc31262c7def1e32a26baed5a577f87d2e72d3598e5387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentTeamId")
    def parent_team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentTeamId"))

    @parent_team_id.setter
    def parent_team_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b82336ff25a8902625acde85763ec1c7754f1da408b967e46722407f576e99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentTeamId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentTeamReadId")
    def parent_team_read_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentTeamReadId"))

    @parent_team_read_id.setter
    def parent_team_read_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2487137cc0ca3e545318468116fae2cbf59872c57dfe7000e8a8dd9903c799e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentTeamReadId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentTeamReadSlug")
    def parent_team_read_slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentTeamReadSlug"))

    @parent_team_read_slug.setter
    def parent_team_read_slug(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da7c18c240cd85fd65e470599d83e001c5bf9295a078f57b1ea4182d6e1cb455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentTeamReadSlug", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privacy")
    def privacy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privacy"))

    @privacy.setter
    def privacy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3ea6ceab6467efc0e04919208cbd88e30ad375010284ba427398318aaa39d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privacy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.team.TeamConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "create_default_maintainer": "createDefaultMaintainer",
        "description": "description",
        "id": "id",
        "ldap_dn": "ldapDn",
        "parent_team_id": "parentTeamId",
        "parent_team_read_id": "parentTeamReadId",
        "parent_team_read_slug": "parentTeamReadSlug",
        "privacy": "privacy",
    },
)
class TeamConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        create_default_maintainer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ldap_dn: typing.Optional[builtins.str] = None,
        parent_team_id: typing.Optional[builtins.str] = None,
        parent_team_read_id: typing.Optional[builtins.str] = None,
        parent_team_read_slug: typing.Optional[builtins.str] = None,
        privacy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the team. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#name Team#name}
        :param create_default_maintainer: Adds a default maintainer to the team. Adds the creating user to the team when 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#create_default_maintainer Team#create_default_maintainer}
        :param description: A description of the team. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#description Team#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#id Team#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ldap_dn: The LDAP Distinguished Name of the group where membership will be synchronized. Only available in GitHub Enterprise Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#ldap_dn Team#ldap_dn}
        :param parent_team_id: The ID or slug of the parent team, if this is a nested team. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#parent_team_id Team#parent_team_id}
        :param parent_team_read_id: The id of the parent team read in Github. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#parent_team_read_id Team#parent_team_read_id}
        :param parent_team_read_slug: The id of the parent team read in Github. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#parent_team_read_slug Team#parent_team_read_slug}
        :param privacy: The level of privacy for the team. Must be one of 'secret' or 'closed'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#privacy Team#privacy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eec23fedc26c961953738789568e377d342aeaa4deb5137bd07e97d19128027)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument create_default_maintainer", value=create_default_maintainer, expected_type=type_hints["create_default_maintainer"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ldap_dn", value=ldap_dn, expected_type=type_hints["ldap_dn"])
            check_type(argname="argument parent_team_id", value=parent_team_id, expected_type=type_hints["parent_team_id"])
            check_type(argname="argument parent_team_read_id", value=parent_team_read_id, expected_type=type_hints["parent_team_read_id"])
            check_type(argname="argument parent_team_read_slug", value=parent_team_read_slug, expected_type=type_hints["parent_team_read_slug"])
            check_type(argname="argument privacy", value=privacy, expected_type=type_hints["privacy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if create_default_maintainer is not None:
            self._values["create_default_maintainer"] = create_default_maintainer
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if ldap_dn is not None:
            self._values["ldap_dn"] = ldap_dn
        if parent_team_id is not None:
            self._values["parent_team_id"] = parent_team_id
        if parent_team_read_id is not None:
            self._values["parent_team_read_id"] = parent_team_read_id
        if parent_team_read_slug is not None:
            self._values["parent_team_read_slug"] = parent_team_read_slug
        if privacy is not None:
            self._values["privacy"] = privacy

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
    def name(self) -> builtins.str:
        '''The name of the team.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#name Team#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def create_default_maintainer(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Adds a default maintainer to the team. Adds the creating user to the team when 'true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#create_default_maintainer Team#create_default_maintainer}
        '''
        result = self._values.get("create_default_maintainer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the team.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#description Team#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#id Team#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ldap_dn(self) -> typing.Optional[builtins.str]:
        '''The LDAP Distinguished Name of the group where membership will be synchronized. Only available in GitHub Enterprise Server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#ldap_dn Team#ldap_dn}
        '''
        result = self._values.get("ldap_dn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_team_id(self) -> typing.Optional[builtins.str]:
        '''The ID or slug of the parent team, if this is a nested team.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#parent_team_id Team#parent_team_id}
        '''
        result = self._values.get("parent_team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_team_read_id(self) -> typing.Optional[builtins.str]:
        '''The id of the parent team read in Github.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#parent_team_read_id Team#parent_team_read_id}
        '''
        result = self._values.get("parent_team_read_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_team_read_slug(self) -> typing.Optional[builtins.str]:
        '''The id of the parent team read in Github.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#parent_team_read_slug Team#parent_team_read_slug}
        '''
        result = self._values.get("parent_team_read_slug")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def privacy(self) -> typing.Optional[builtins.str]:
        '''The level of privacy for the team. Must be one of 'secret' or 'closed'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/team#privacy Team#privacy}
        '''
        result = self._values.get("privacy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Team",
    "TeamConfig",
]

publication.publish()

def _typecheckingstub__fca448c41b9f6dc955ef80a805cab1cb3ed4f5b0c5c4db093e32387f385ff10b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    create_default_maintainer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ldap_dn: typing.Optional[builtins.str] = None,
    parent_team_id: typing.Optional[builtins.str] = None,
    parent_team_read_id: typing.Optional[builtins.str] = None,
    parent_team_read_slug: typing.Optional[builtins.str] = None,
    privacy: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__2e6458102f84c8ac1b2ded755f46a8cd3a0abfa324384cd105ec6532b6621563(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862ef8eb06d2c76c2ba5433f21ff71e9f8dd1585051cbb18367b5b4b8af0f0c1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b976fe33bc6083fb7b0ca946b844bc4e20b4b8e8736cd4cd51c997084002a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc18b193d1fa5a2c5c81f741b77037276ae0bee5016c349469aefc36d34e85d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab7e4949bd85d85e39b252323c6e82b63336a6e4046b9c7bae800dc683ce84e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3a056c0ad8a48baffc31262c7def1e32a26baed5a577f87d2e72d3598e5387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b82336ff25a8902625acde85763ec1c7754f1da408b967e46722407f576e99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2487137cc0ca3e545318468116fae2cbf59872c57dfe7000e8a8dd9903c799e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7c18c240cd85fd65e470599d83e001c5bf9295a078f57b1ea4182d6e1cb455(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3ea6ceab6467efc0e04919208cbd88e30ad375010284ba427398318aaa39d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eec23fedc26c961953738789568e377d342aeaa4deb5137bd07e97d19128027(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    create_default_maintainer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ldap_dn: typing.Optional[builtins.str] = None,
    parent_team_id: typing.Optional[builtins.str] = None,
    parent_team_read_id: typing.Optional[builtins.str] = None,
    parent_team_read_slug: typing.Optional[builtins.str] = None,
    privacy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
